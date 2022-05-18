# 写在前面：
# 函数myd()计算日期是否符合标准(不去除未来，去除类似于20050229,20050000之类的。
# 函数g()粗略计算地区是否存在，但事实上可能是少忽略了一些情况。
# 函数f()根据身份证加权码进行较为复杂的身份证计算。
# 注：身份证加权码可计算，w[i]=(2^(17-i))%11 (i∈(0,18)∩N)，为减少运算量，因此略去。
def myd(x):
	a=int(x[6:10]); #年份
	b1=int(x[10:12]); #月份
	b2=int(x[12:14]); #日
	if a%4==0: #分析是否为闰年
		if a%100==0 and a%400!=0:
			m2=0;
		else:
			m2=1;
	else:
		m2=0;
	md=[31,28,31,30,31,30,31,31,30,31,30,31];
	if m2==1:
		md[1]=29; #闰年2月为29天
	else:
		pass;
	if b1<1 or b2<1 or b1>12 or md[b1-1]<b2: #多种情况讨论是否符合日期常识
		return 0;
	else:
		return 1;
def g(x):
	if 0<int(x[0])<7 and myd(x)==1: #当地区码和日期全部通过时
		return 1;
	else: 
		return 0;
def f(idcardnumber,mode): #mode的意义详见函数体后的主程序部分
	c=0;
	w=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2,1]; #引入身份证加权码
	o=0;
	d=[];
	u=[0]; #缺失位置列表，首位元素为后面元素的数量，其他位置为残缺的位置
	everyposition=[];
	for i in range(0,18):
		everyposition.extend(idcardnumber[i]); #将得到的身份证号码的每一位分别存到列表中
		if idcardnumber[i].isdigit(): #当字符串内容是数字时，该函数返回Ture
			c+=w[i]*int(idcardnumber[i]); #加权求和
		else:
			if idcardnumber[i]=="X": #X等价于10
				c+=10;
			else:
				u.extend([i]); #其他字符时，记录数量，记录位置
				u[0]+=1;
	if mode==0: 
		a=[0]; #结果列表，首位元素为后面元素的数量
		if u[-1]==17: #最后一位缺失时
			for i in range(0,10**(u[0]-1)):
				fff=c; #为穷举铺垫，保证每次的原已有加权和正确
				strccc=str(i).zfill(u[0]-1); #字符串，补全位数
				for o in range(0,u[0]-1):
					fff+=int(strccc[o])*w[u[o+1]]; #穷举加权运算
				for k in range(0,11): #上面均不含最后一位，此处为最后一位的穷举
					if (fff+k)%11==1: #符合身份证规则
						gs=0; #进行记录是第几次导出的变量，每次归零
						for o in u[1:u[0]]: 
							everyposition[o]=strccc[gs]; #导入每缺失位（除最后一位）的结果列表
							gs+=1; 
						if k==10: #对结果位是否为X的讨论
							everyposition[17]="X";
						else:
							everyposition[17]=str(k);
						a[0]+=1; #记录成功位数
						a.extend([""]) #定义新元素
						for o in range(0,18):
							a[a[0]]=a[a[0]]+everyposition[o]; #按位置，逐一导入字符
		else: #最后一位已经存在时
			for i in range(0,10**u[0]):
				fff=c; #为穷举铺垫，保证每次的原已有加权和正确
				strccc=str(i).zfill(u[0]); #字符串，补全位数
				for o in range(0,u[0]):
					fff+=int(strccc[o])*w[u[o+1]];  #穷举加权运算
				if fff%11==1: #符合身份证规则
					gs=0; #进行记录是第几次导出的变量，每次归零
					for o in u[1:u[0]+1]:
						everyposition[o]=strccc[gs]; #导入每缺失位的结果列表
						gs+=1;
					a[0]+=1; #记录成功位数
					a.extend([""]); #添加一个空的新元素
					for o in range(0,18):
						a[a[0]]=a[a[0]]+everyposition[o]; #按位置，逐一导入字符
				else:
					pass;
		da=[0] #不合理情况列表，首位元素为后面元素的数量
		for i in range(1,a[0]+1):
			if g(a[i])==0: #验证错误
				da[0]+=1;
				da.extend([a[i]])
			else:
				pass;
		a[0]-=da[0]; #减去失败的数量
		for i in range(1,da[0]+1):
			a.remove(da[i]); #以元素内容查找，删除元素及其位置
	else: #比较计算的验证码和已知验证码是否相同以判断身份证是否合理
		if idcardnumber[i]=="X":
			c-=10;
		else:
			c-=int(idcardnumber[17]);
		c=(12-(c%11))%11;
		if c<10:
			a=idcardnumber[0:17]+str(c);
		else:
			a=idcardnumber[0:17]+"X";
	return a; #返回结果：列表(mode==0)或字符串(mode==1)
d="补全身份证号码请输0，检验身份证号码请输1，输入其他以退出：";
b="验证的结果是：";
e="。";
a=int(input(d));
while a==0 or a==1:
	if not a:
		c=input("请输入残缺的身份证号码（空缺位置用一个任意除X以外的非数字字符代替）：");\
		list1=f(c,a);
		print("共有"+str(list1[0])+"种可能，如下：");
		for i in range(0,list1[0]):
			print(list1[i+1]);
		print("至此，"+str(list1[0])+"种可能已计算完毕。");
	elif a:
		c=input("请输入要验证的身份证号码：");
		if f(c,a)==c and g(c)==1:
			print(b+"正确"+e);
		else:
			print(b+"错误"+e);
	a=int(input(d));
# 写在最后：
# 这是本人的第一个成型代码，很多东西并不是很智能，穷举耗费大量时间
# 这些我都是知道的，但是毕竟现在很菜，见谅见谅
# 灵感来源于李永乐老师的一期关于身份证的视频，详见
# https://www.bilibili.com/video/BV1U7411p7WH
#（史上最靓身份证号即将诞生！李永乐老师揭秘身份证号码的秘密）