theta=linspace(0,360,1000);
theta_rot = 45;
k=.04;
a=.3;
b=5;
rf=[];
r=zeros(1000,1);
x=zeros(1000,1);
y=zeros(1000,1);
scaler=[1 2, 3 4];

for i=1:1000
   r(i)=k*((cosd(theta(i))).^2+a*cosd(theta(i))+b);
end

for i =1:1000
    x(i)=r(i)*cosd(theta(i));
    y(i)=r(i)*sind(theta(i));
end

cam_points=[x y];
cam1=cam_points;
cam6=ro(cam1,0,14,0);
a=45;
b=90;
c=135;
d=30;


for count =1:50
 r4 = randperm(360,7);
 cam2=ro(cam1,90,0,0);
 cam3=ro(cam1,r4(1),3,0.15);
 cam4=ro(cam1,r4(2),6,0.25);
 cam5=ro(cam1,r4(3),10,0.13);
 cam7=ro(cam1,r4(4),12,-0.15);
 cam8=ro(cam1,r4(5),9,-0.2);
 cam9=ro(cam1,r4(6),7,-0.22);
 cam11=ro(cam1,r4(7),1.5,-0.13);



for i=1

hold on

plot(cam3(:,1),cam3(:,2))
plot(cam4(:,1),cam4(:,2))
plot(cam5(:,1),cam5(:,2))
plot(cam7(:,1),cam7(:,2))
plot(cam8(:,1),cam8(:,2))
plot(cam9(:,1),cam9(:,2))
plot(cam11(:,1),cam11(:,2))
plot(scaler(:,1),scaler(:,2))
rf=interp(conv(cam1),conv(cam3),conv(cam4),conv(cam5),conv(cam6),conv(cam7),conv(cam8),conv(cam9),conv(cam11),r4,count,rf);
drawnow

end
end

function ro=ro(a,theta,b,c)
   a1=[];
   R = [cosd(theta),-sind(theta); sind(theta), cosd(theta)];
   
   a1=(R*a')';
   
   ro(:,1)=a1(:,1)+b;
   ro(:,2)=a1(:,2)+c;
end

function conv=conv(a)
  for i=1:1000
      if abs(a(i,2))==max(abs(a(:,2)))
          conv=[a(i,1) a(i,2)];
      end
  end
end

function rf=interp(a,b,c,d,e,f,g,h,i,r4,count,rf)
   interp(:,1)=[a(1,1) b(1,1) c(1,1) d(1,1) e(1,1)];
   interp(:,2)=[a(1,2) b(1,2) c(1,2) d(1,2) e(1,2)];
   interpi(:,1)=[a(1,1) f(1,1) g(1,1) h(1,1) i(1,1)  e(1,1)];
   interpi(:,2)=[a(1,2) f(1,2) g(1,2) h(1,2) i(1,2)  e(1,2)];   
   x = interp(:,1);
   y =  interp(:,2);
   x1 = interpi(:,1);
   y1 =  interpi(:,2);
   xx1 = 0:.25:14;
   xx = 0:.25:14;  
   yy = spline(x,y,xx);
   yy1 = spline(x1,y1,xx1);
   k= [flip(xx),xx1(1,2:57);flip(yy),yy1(1,2:57)];
   k=k';
   rf(end+1,:)=r4;
  
   filename = [num2str(count), '.dat']
  
   save 'filename' k -ascii ;   
   csvwrite('LEtsgo.csv',rf);
   hold on
   plot(x,y,'o',xx,yy);
   plot(x1,y1,'o',xx1,yy1);
end



