lines(0)

disp("Example 2.1")
printf("\n")
printf("Given")
disp("Resistance used is 4 ohm")
disp("Current flow is i=2.5*sin(w*t)")
disp("Angular frequency(w)=500 rad/s")

R=4;
iamp=2.5;w=500;
t=0:0.001:0.012566
i=2.5*sin(w*t)


Vamp=iamp*R;
printf("v=%d*sin(%d*t)(V)\n",Vamp,w)

pamp=iamp*iamp*R;
printf("p=%d(sin(%d*t))^2(W)\n",pamp,w)
p=pamp*sin(w*t)^2;

//On integrating p with respect to t
W=25*(t/2-sin(2*w*t)/(4*w))

function p=f(t),p=pamp*sin(w*t)^2,endfunction
w1=intg(0,2*%pi/w,f);


subplot(221)
plot(t,i)
xs2jpg(gcf(), "/home/cheese/cloud/soc/static/tmp/1387919154.jpg");
xtitle ('i vs wt','wt','i ');

subplot(222)
plot(t,p)
xs2jpg(gcf(), "/home/cheese/cloud/soc/static/tmp/1387919155.jpg");
xtitle ('p vs wt','wt','p ');



subplot(223)
plot(t,W)
xs2jpg(gcf(), "/home/cheese/cloud/soc/static/tmp/1387919156.jpg");
xtitle ('w vs wt','wt','w ');


exit
