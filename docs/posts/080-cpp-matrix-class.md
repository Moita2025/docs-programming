---
date: 2026-06-07
authors:
  - moita
categories:
  - 算法
  - 工程实践
tags:
  - CPP
  - 数据结构
  - 面向对象
---

# C++ 矩阵运算类

一个完整的 C++ 矩阵类实现，包含构造/拷贝/析构、运算符重载、转置、行列式、伴随矩阵、求逆、高斯消元、QR 分解、特征值与特征向量等功能。代码体量较大但存在多处逻辑错误。

<!-- more -->

## 六处关键错误

### 1. 析构函数中对同一指针重复 delete

```cpp
Matrix::~Matrix()
{
    for(int i = 0;i < row * col;i++)    // 错误：循环 delete 同一个指针
        delete[] matrix;
}
```

`matrix` 由一次 `new[]` 分配，只需一次 `delete[]`。循环内反复释放同一块内存会直接崩溃。修正为：

```cpp
Matrix::~Matrix()
{
    delete[] matrix;                    // 修正：仅释放一次
}
```

### 2. swapRows 只交换单个元素

```cpp
void Matrix::swapRows(int a, int b)
{
    a--;
    b--;
    double temp = matrix[a];           // 错误：只交换了 matrix[a] 和 matrix[b] 两个元素
    matrix[a] = matrix[b];
    matrix[b] = temp;
}
```

行交换需要交换整行的所有列元素，这里只交换了扁平数组中两个不相关位置的值。修正为逐列交换：

```cpp
void Matrix::swapRows(int a, int b)     // 修正：逐列交换整行
{
    a--;
    b--;
    for (int j = 0; j < col; j++)
    {
        double temp = matrix[a * col + j];
        matrix[a * col + j] = matrix[b * col + j];
        matrix[b * col + j] = temp;
    }
}
```

### 3. operator*= 计算了结果但未写回

```cpp
Matrix &Matrix::operator*=(const Matrix &m)
{
    // ... 创建 te 并计算 te = (*this) * m ...
    Matrix te(row, m.col);
    // ... 乘法运算填入 te ...
    return *this;                       // 错误：te 的结果从未赋给 *this
}
```

`*this` 从未被修改，`*=` 等于没做。修正：将 `te` 的结果写回 `*this` 并调整行列尺寸。

```cpp
Matrix &Matrix::operator*=(const Matrix &m)
{
    if (col != m.row) return *this;
    Matrix te(row, m.col);
    for (int i = 0; i < row; i++)
        for (int j = 0; j < m.col; j++)
            for (int k = 0; k < col; k++)
                te.matrix[i * m.col + j] += matrix[i * col + k] * m.matrix[k * m.col + j];

    delete[] matrix;                     // 新增：释放旧数据
    matrix = te.matrix;                  // 新增：接管 te 的数据
    te.matrix = NULL;                    // 新增：防止 te 析构时释放
    col = m.col;
    quantity = row * col;
    return *this;
}
```

### 4. solveAb 返回了错误的变量

```cpp
Matrix solveAb(Matrix &m1, Matrix &m2)
{
    // ...
    Matrix invA(m1.col, m1.row);
    invA += m1.inverse();
    Matrix result(invA.row, m2.col);
    result += invA * m2;                // result = A⁻¹ * b
    return invA;                        // 错误：返回的是 A⁻¹ 而非 A⁻¹*b
}
```

解方程 Ax = b 时应返回 `result`（即 A⁻¹b），函数却返回了 `invA`（仅逆矩阵本身）。修正：`return invA;` 改为 `return result;`。

### 5. operator- 维度检查始终为真

```cpp
Matrix operator-(const Matrix &m1, const Matrix &m2)
{
    if(m1.row!=m2.row||m1.col!=m1.col)  // 错误：m1.col != m1.col 恒为 false
    // ...
}
```

`m1.col != m1.col` 永远为假，列维度检查形同虚设。修正为 `m1.col != m2.col`。

### 6. AlgCofactor 中列偏移计算错误

```cpp
int temcol = j < n ? 1 : 1;            // 错误：两个分支都是 1
```

计算代数余子式时，子矩阵应跳过第 n 列。三元表达式两个分支都返回 1，意味着无论 j 是否小于 n 都会偏移一列，导致余子式取错元素。修正：

```cpp
int temcol = j < n ? 0 : 1;            // 修正：j < n 时不偏移，j >= n 时跳过一列
```

---

## 其余可改进之处

**头文件冗余**：`<stdio.h>` 与 `<cstdio>`、`<math.h>` 与 `<cmath>` 同时包含，保留 C++ 版本 `<cstdio>`、`<cmath>` 即可。

**`initmatrix` 分配大小错误**：`new double[row]` 应为 `new double[row * col]`。该函数虽未被调用，但定义存在隐患。

**`rank` 函数设计**：`rank` 是成员函数却以另一个矩阵为参数，内部也不使用 `this`。完成高斯消元后直接统计非全零行即可。

六处错误中，析构函数和 swapRows 会在运行时直接导致崩溃或错误结果；operator*= 和 solveAb 返回值逻辑错误会让调用者拿到完全错误的数据；AlgCofactor 则影响伴随矩阵和求逆的精度。其余几处属于代码规范层面的改善。

---

## 原始代码

```cpp
#include <stdio.h>
#include <cstdio>
#include <iostream>
#include <math.h>
#include <cmath>
#include <stdlib.h>

using namespace std;

const double EPS = 1e-10;

class Matrix
{
	
	public:
		int row;
		int col;
		int quantity;
		double *matrix;
		Matrix(int r,int c):row(r),col(c)//构造函数
	    {
	        quantity = r*c;
	        if (quantity > 0)
	        {
	            matrix = new double[quantity];
	        }
	        else
	            matrix = NULL;
	    };
		Matrix(const Matrix &rhs)//拷贝构造
	    {
	        row = rhs.row;
	        col = rhs.col;
	        quantity = rhs.quantity;
	        matrix = new double[quantity];
	        for (int i = 0; i < quantity; i++)
	            matrix[i] = rhs.matrix[i];
	    }
		virtual ~Matrix();
		void initmatrix();
		Matrix inverse();//矩阵的逆 
		
		int rank(const Matrix&);
		 
		Matrix  &operator=(const Matrix&); 
		double& operator()(int m,int n);//利用（）运算符重载可以改变某个矩阵元素的值
		friend Matrix solveAb(Matrix &,Matrix &); 
		//friend Matrix operator=(Matrix &,Matrix &);
		friend Matrix operator/(const Matrix&, double);
		friend istream &operator>>(istream&, Matrix&);
		friend ostream &operator<<(ostream&, Matrix&);
   		friend Matrix  operator+(const Matrix&, const Matrix&);
		friend Matrix operator-(const Matrix&, const Matrix&);
		friend Matrix operator*(const Matrix&, const Matrix&); 
		friend Matrix  operator*(double, const Matrix&);  //数乘矩阵
    	friend Matrix  operator*(const Matrix&, double);  //矩阵乘数 
		Matrix operator=(double *);
		Matrix& operator+=(const Matrix &m1);
		Matrix& operator-=(const Matrix &);
		Matrix& operator*=(const Matrix &m1);
		double*operator[](int i){ return matrix + i*col; }
		Matrix  transpose()const;//矩阵转置 
		double determinant();//矩阵行列式
		Matrix Adjugate();
		void swapRows(int, int);
 		Matrix gaussianEliminate();//高斯消元法 const Matrix &m
 		
 		Matrix diag();
 		void QR(Matrix&, Matrix&)const;
   		Matrix eig_val(int _iters = 1000);
    	Matrix eig_vect(int _iters = 1000);
		friend void menu();
}; 
 
Matrix::~Matrix()//析构函数 
{
	for(int i = 0;i < row * col;i++)
		delete[] matrix;
}
void Matrix::initmatrix()//初始化矩阵 
{
	int i,j;
	matrix = new double[row];
	for(i = 0;i < row * col;i++)
		matrix[i]=0.00;
}
double& Matrix::operator()(int m,int n)
{
	return *(matrix + m * col + n); 
}
Matrix&  Matrix::operator=(const Matrix& rhs)
{
    if (this != &rhs)
    {
        row = rhs.row;
        col = rhs.col;
        quantity = rhs.quantity;
        if (matrix != NULL)
            delete[] matrix;
        matrix = new double[quantity];
        for (int i = 0;i < quantity;i++)
        {
            matrix[i] = rhs.matrix[i];
        }
    }
    //cout<<"ok";
    return *this;
}
 
istream& operator>>(istream &is, Matrix &obj)
{
    for(int i = 0;i < obj.row * obj.col;i++)
    {
        is >> obj.matrix[i];
    }
    return is;
}
ostream& operator<<(ostream &out, Matrix &obj)
{
    for (int i = 0;i < obj.row;i++) //打印矩阵
    {
        for(int j = 0;j < obj.col;j++)
        {
            out<<(obj[i][j])<<"\t";
        }
        out<<endl;
    }
    return out;
}
Matrix operator+(const Matrix& m1,const Matrix& m2)
{
    if (m1.col!=m2.col||m1.row!=m2.row)
    {
        Matrix temp(0, 0);
        temp.matrix=NULL;
        cout <<"矩阵不合法"<<endl;
        return temp;
    }
    Matrix ret(m1.row, m1.col);
    for (int i=0;i<ret.quantity;i++)
    {
        ret.matrix[i]=m1.matrix[i]+m2.matrix[i];
    }
    return ret;
}
 
Matrix operator-(const Matrix &m1, const Matrix &m2)
{
	if(m1.row!=m2.row||m1.col!=m1.col)
	{
		Matrix temp(0,0);
		cout<<"矩阵不合法"<<endl;
		return temp;
	}
	Matrix te(m1.row,m1.col);
	for(int i=0;i<m1.row*m1.col;i++)
		te.matrix[i]=m1.matrix[i]-m2.matrix[i];
	return te;
}
Matrix  operator*(const Matrix& m1, const Matrix& m2)
{
    if (m1.quantity==0||m2.quantity==0||m1.col!=m2.row)
    {
        Matrix temp(0,0);
        temp.matrix=NULL;
        cout<<"矩阵不合法"<<endl;
        return temp; //数据不合法时候，返回空矩阵
    }
    Matrix ret(m1.row,m2.col);
    for (int i=0;i<m1.row;i++)
    {
        for (int j=0;j<m2.col;j++)
        {
            for (int k=0;k<m1.col;k++)//m1.col == m2.row
            {
                ret.matrix[i*m2.col+j]+=m1.matrix[i*m1.col+k]*m2.matrix[k*m2.col+j];
            }
        }
    }
    return ret;
}
Matrix operator*(double val, const Matrix& m)  //矩阵乘 单数
{
    Matrix ret(m.row, m.col);
    for (int i=0;i<ret.quantity;i++)
    {
        ret.matrix[i]=val*m.matrix[i];
    }
    return ret;
}
Matrix operator*(const Matrix&m,double val)  //矩阵乘 单数
{
    Matrix ret(m.row,m.col);
    for (int i=0;i<ret.quantity;i++)
    {
        ret.matrix[i]=val*m.matrix[i];
    }
    return ret;
}
Matrix &Matrix::operator+=(const Matrix &m1)
{
	int i;
	for(i=0;i<m1.col*m1.row;i++)
		matrix[i]=matrix[i]+m1.matrix[i];
	return *this; 
}
Matrix &Matrix::operator-=(const Matrix &m1)
{
	int i;
	for(i=0;i<m1.col*m1.row;i++)
		matrix[i]=matrix[i]-m1.matrix[i];
	return *this; 
}
Matrix &Matrix::operator*=(const Matrix &m)
{
	int i,j,k;
	if(col==0||row==0||m.col==0||row==0||col!=m.row)
	{
		Matrix temp(0,0);
		cout<<"矩阵不合法"<<endl;
		return *this;	
	 } 
	 Matrix te(row,m.col);
	 for (i=0;i<row;i++)
    {    for (j=0;j<m.col;j++)
        {   for (k=0;k<col;k++)
            {
                te.matrix[i*m.col+j]+=matrix[i*col+k]*m.matrix[k*m.col+j];
            }
        }
    }
	return *this;
}
 
Matrix Matrix::transpose()const//实现矩阵的转置操作 
{
	int k=0;
    Matrix tem(col,row);
    for (int i=0;i<row;i++)
    {
        for (int j=0;j<col;j++)
        {
            tem[j][i]=matrix[i*col+j];
        }
    }
    return tem;
}
double calcDet(int n,double *&aa)
{
    if (n==1)
        return aa[0];
    double *bb=new double[(n-1)*(n-1)];
    double sum=0.00;
    for (int Ai=0;Ai<n;Ai++)
    {
        for (int Bi=0;Bi<n-1;Bi++)
        {
            int offset= Bi<Ai?0:1; 
            for (int j=0;j<n-1;j++)
            {
                bb[Bi*(n-1)+j]=aa[(Bi+offset)*n+j+1];
            }
        }
        int flag=(Ai%2==0?1:-1);
        sum+= flag*aa[Ai*n]*calcDet(n-1,bb);
    }
    delete[]bb;
    return sum;
}
double Matrix::determinant()
{
    if (col==row)
        return calcDet(row,matrix);
    else
    {
        cout<<"矩阵不合法"<<endl;
        return 0;
    }
}
double AlgCofactor(Matrix& mt, int m, int n)//代数余子式 
{
	int trow=mt.row-1;
	Matrix temp(trow,trow);
	for(int i=0;i<trow;i++)
		for(int j=0;j<trow;j++)
		{
			int temrow=i<m?0:1;
			int temcol=j<n?1:1;
			temp[i][j]=mt[i + temrow][j + temcol];
		}
		int flag;
		flag=(m+n)%2==0?1:-1;
		return flag*temp.determinant();
}
Matrix Matrix::Adjugate()//伴随矩阵 
{
	int i,j,k;
	if(col!=row)
	{
		Matrix tem(0,0);
		cout<<"矩阵不合法"<<endl;
		return tem;
	}
	Matrix temp(row,col);
	for(i=0;i<row;i++)
		for(j=0;j<col;j++) 
		temp.matrix[j*row+i]= AlgCofactor(*this,i,j);
	return temp;
}
Matrix operator/(const Matrix& m1, double n)  //矩阵除以单数
{
    Matrix ret(m1.row,m1.col);
    for (int i=0;i<ret.row*ret.col;i++)
    {
        ret.matrix[i]= m1.matrix[i]/n;
    }
    return ret;
}
 
Matrix Matrix::inverse()
{
    double det=determinant();
    if (det==0)
    {
        cout << "行列式为0，不能计算逆矩阵。" << endl;
        return Matrix(0,0);
    }
    return Adjugate()/det;
}
Matrix solveAb(Matrix &m1,Matrix &m2)
{
	if(m1.row==0||m1.col==0||m2.row==0||m2.col==0)
	{
		Matrix tem(0,0);	
		cout<<"矩阵不合法"<<endl;
		return tem;
	}
	Matrix invA(m1.col,m1.row);
	invA+=m1.inverse();
	Matrix result(invA.row,m2.col);
	result+=invA*m2;	
	return invA;
}
 
//实现行变换
void Matrix::swapRows(int a, int b)
{
	a--;
	b--;
	double temp = matrix[a];
	matrix[a] = matrix[b];
	matrix[b] = temp;
}
Matrix Matrix::gaussianEliminate()
{
	Matrix Ab(*this);
	int rows=Ab.row;
	int cols=Ab.col;
	int Acols= cols-1;
 
	int i=0; //跟踪行
	int j=0; //跟踪列
	while (i<rows)
	{
		bool flag=false;
		while (j<Acols&&!flag)
		{
			if (Ab[i][j]!=0) {
				flag=true;
			}
			else {
				int max_row=i;
				double max_val=0;
				for (int k=i+1;k<rows;++k)
				{
					double cur_abs=Ab[k][j]>=0?Ab[k][j]:-1*Ab[k][j];
					if (cur_abs>max_val)
					{
						max_row=k;
						max_val=cur_abs;
					}
				}
				if (max_row!=i){
					Ab.swapRows(max_row, i);
					flag=true;
				}
				else {
					j++;
				}
			}
		}
		if (flag)
		{
			for (int t=i+1;t<rows;t++) {
				for (int s=j+1;s<cols;s++) {
					Ab[t][s]=Ab[t][s]-Ab[i][s]*(Ab[t][j]/Ab[i][j]);
					if (abs(Ab[t][s])<1e-10)
						Ab[t][s] = 0;
				}
				Ab[t][j]=0;
			}
		}
		i++;
		j++;
	}
	//cout<<Ab;
	return Ab;
}
 
int Matrix::rank(const Matrix &m)
{
	int i,j;
	int num,count; 
	Matrix temp(m.row,m.col);
	temp=m;count=0;
	//cout<<"阶梯矩阵:\n"<<temp;
	for(i=0;i<m.row;i++)
	{
		num=0;
		for(j=0;j<m.col;j++)
		{
			if(temp[i][j]==0) num++;
		}
		if(num!=temp.col)
		count++;
	}	
	return count;
}
void  Matrix::QR(Matrix &Q, Matrix &R) const
{
    if (row!= col)
    {
        printf("矩阵不合法\n");
        return;
    }
    const int N=row;
    double *a=new double[N];
    double *b=new double[N];
 
    for(int j=0;j<N;++j)  
    {
        for(int i=0; i<N;++i)  
            a[i]=b[i]=matrix[i*N+j];
 
        for(int i=0;i<j;++i)  
        {
            R.matrix[i*N+j]=0;  
            for(int m=0;m<N;++m)
            {
                R.matrix[i*N+j]+=a[m]*Q.matrix[m*N+i]; 
            }
            for(int m=0;m<N;++m)
            {
                b[m]-=R.matrix[i*N+j]*Q.matrix[m*N+i];
            }
        }
        double norm=0;
        for(int i=0;i<N;++i)
        {
            norm+=b[i]*b[i];
        }
        norm=(double)sqrt(norm);
        R.matrix[j*N+j]=norm; 
        for (int i=0;i<N;++i)
        {
            Q.matrix[i*N+j]=b[i]/norm; 
        }
    }
    delete[]a;
    delete[]b;
}
Matrix Matrix::diag()
{
    if (row!=col)
    {
        Matrix m(0,0);
        cout<<"矩阵不合法"<<endl;
        return m;
    }
    Matrix m(row,row);
    for(int i=0;i<row;i++)
    {
        m.matrix[i*row+i]=matrix[i*row+ i];
    }
    return m;
}
Matrix Matrix::eig_val(int _iters)
{
    if (quantity==0||row!=col)
    {
        cout<<"矩阵为空或者非方阵！"<< endl;
        Matrix rets(0,0);
        return rets;
    }
    const int N=row;
    Matrix matcopy(*this);//备份矩阵
    Matrix Q(N,N),R(N,N);
 
    for (int k=0;k<_iters;++k)
    {
        
        QR(Q,R);
        *this=R*Q;
 
    }
    Matrix val=diag();
    *this=matcopy;//恢复原始矩阵；
    return val;
}
Matrix Matrix::eig_vect(int _iters)
{
    if(quantity==0||row!=col)
    {
        cout<<"矩阵为空或者非方阵！"<<endl;
        Matrix rets(0,0);
        return rets;
    }
    if(determinant()==0)
    {
      cout <<"非满秩矩阵无法分解计算特征向量！"<<endl;
      Matrix rets(0,0);
      return rets;
    }
    Matrix matcopy(*this);
    Matrix eigenValue=eig_val(_iters);
    Matrix ret(row,row);
    const int NUM=col;
    double eValue;
    double sum,midSum,diag;
    Matrix copym(*this);
    for(int count=0;count<NUM;++count)
    {
        *this=copym;
        eValue=eigenValue[count][count];
        for(int i=0;i<col;++i)//A-lambda*I
        {
            matrix[i*col+i]-=eValue;
        }
        for(int i=0;i<row-1;++i)
        {
            diag=matrix[i*col+i]; 
            for(int j=i;j<col;++j)
            {
                matrix[i*col+j]/=diag; 
            }
            for (int j=i+1;j<row;++j)
            {
                diag=matrix[j*col+ i];
                for (int q=i;q<col;++q)
                {
                    matrix[j*col+q]-=diag*matrix[i*col+q];
                }
            }
        }
        midSum=ret.matrix[(ret.row-1)*ret.col+count]=1;
        for (int m=row-2;m>=0;--m)
        {
            sum=0;
            for(int j=m+1;j<col;++j)
            {
                sum+=matrix[m*col+j]*ret.matrix[j*ret.col+count];
            }
            sum=-sum/matrix[m*col+m];
            midSum+=sum*sum;
            ret.matrix[m*ret.col+count]=sum;
        }
        midSum=sqrt(midSum);
        for (int i=0;i<ret.row;++i)
        {
            ret.matrix[i*ret.col+count]/=midSum; 
        }
    }
    *this=matcopy;
    return ret;
}
void menu()
{
	cout<<"选择："<<endl;
	cout<<"1.+"<<endl<<"2.-"<<endl<<"3.*"<<endl;
	cout<<"4.求逆"<<endl<<"5.求行列式  \n6.矩阵的转置" <<endl;
	cout<<"7.AX=b求解操作"<<endl;
	cout<<"8.利用（）运算符重载可以改变某个矩阵元素的值\n";
	cout<<"9.求矩阵的秩\n";
	cout<<"请输入：";
	int i;int n=3;
	cin>>i;
	Matrix a(n,n);
	//cin>>a;
	
	Matrix c(n,n);
	switch(i) {
		case 1:{
			cout<<"请输入矩阵："<<endl;
			cin>>a;
			Matrix b(n,n);
			cin>>b;
				c=a+b;cout<<"a+b:\n"<<c;
			break;
		}
		case 2:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
			Matrix b(n,n);
			cin>>b;
				c=a-b;
				cout<<"a-b:\n"<<c;
			break;
		}
		case 3:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
			Matrix b(n,n);
			cin>>b;
			c=a*b;cout<<"a*b:\n"<<c;
			break;
		}
		case 4:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
				c=a.inverse();
				cout<<"矩阵a的逆\n"<<endl<<c<<endl;
			break;
		}
		case 5:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
			int det;
			det=a.determinant();
			cout<<"a的行列式:\n"<<det<<endl;
			break;
		}
		case 6:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
			c=a.transpose();
			cout<<"实现矩阵的转置操作\n"<<c<<endl;
			break;
		}
		case 7:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
			Matrix b(n,n);
			cin>>b;
			c=solveAb(a,b);
			cout<<"实现AX=b求解操作\n"<<endl;cout<<c; 
			break;
		}
		case 8:{
				cout<<"请输入矩阵："<<endl;
			cin>>a;
			int i,j,n;
			cout<<"利用（）运算符重载可以改变某个矩阵元素的值"<<endl;
			cout<<"请输入row："<<endl; cin>>i;
			cout<<"请输入col："<<endl; cin>>j;
			cout<<"请输入n："<<endl; cin>>n;
			a(i,j)=n; //利用（）运算符重载可以改变某个矩阵元素的值
			break;
		}
		case 9:{
			
			int r;
			cout<<"请输入矩阵："<<endl;
			cin>>a;
			Matrix temp(n,n);
			temp=a.gaussianEliminate();
			cout<<"temp\n"<<temp;
			r=a.rank(temp);
			cout<<endl;
			cout<<r<<endl;
			break;
		}
	}
		
}
int main()
{
 
	int choose=1;
	menu();
	while(choose)
	{
		cout<<"是否继续：1.继续；0.退出\n";
		cin>>choose;
		if(choose==1)
			menu();
		else
			break;
	}
	 
	return 0;
 } 
```