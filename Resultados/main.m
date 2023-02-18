% Proyecto Sistemas Electrónicos Integrados 
%
% Localizador GPS Para Ganado mediante LoRa
%
% David Fernández Martínez (davidfm8@correo.ugr.es)
% Rafael Adán López        (rafadan6@correo.ugr.es)
% 
% Este script recibe el fichero generado en Node Red que contiene todos
% los mensajes recibidos durante el tiempo de funcionamiento del servidor
% local y representa los resultados obtenidos

clear all;
clc;
close all;

%data = readmatrix('Version_simple.xlsx');   % Versión simple (sin acel)
data= readmatrix('Version_avanzada.xlsx');  % Versión con acelerómetro


% Se define la posición del gateway durante las pruebas
latgw=37.168965;
longw=-3.539765;

% Se extraen los datos por separado
data=data(2:end,2:end);
lat=data(:,1);
lon=data(:,2);
battery=data(:,3);
hora=data(:,4:end);


[m,n]=size(hora);

% Se calcula el tiempo total de funcionamiento a partir de la hora recibida
% en cada mensaje
t=[];
t(1)=0;
k=2;
dif_time=[];
for i=2:m
   h_actual=hora(i,1);
   h_ant=hora(i-1,1);
   min_actual=hora(i,2);
   min_ant=hora(i-1,2);
   seg_actual=hora(i,3);
   seg_ant=hora(i-1,3);
   
   time_actual=h_actual*3600+min_actual*60+seg_actual;
   time_ant=h_ant*3600+min_ant*60+seg_ant;
   dif_time(i)=time_actual-time_ant;
   
   t(k)=t(k-1)+dif_time(i);
   k=k+1;
end


% Se calcula la distancia entre el nodo y el gateway en cada mensaje a
% partir de los valores de latitud y longitud

distancia=[];
for i=1:length(lat)
   nodo=txsite('Name','nodo','Latitude',lat(i),'Longitude',lon(i));
   gateway=rxsite('Name','Gateway','Latitude',latgw,'Longitude',longw);
   distancia(i)=distance(nodo,gateway,'euclidean');
end

figure(1)
plot(t/60,battery)
xlabel('tiempo (min)')
ylabel('Voltaje')
grid on
title('Consumo de bateria')

figure(2)
plot(t/60,distancia)
xlabel('tiempo(min)')
ylabel('Distancia (m)')
grid on
title('Distancia nodo-gateway')
dist_max=max(distancia);
text(1,800,strcat("Distancia máxima= ",num2str(dist_max),"m"))

figure(3)
h=geoplot(lat,lon);
geobasemap satellite
h.Marker="o";
h.MarkerSize=2;
h.MarkerFaceColor="m";
h.LineWidth=1;
h.Color="b";
title("Recorrido realizado durante la prueba")

figure(4)
histogram(dif_time,30)
title('Tiempo entre mensajes consecutivos')
xlabel(' Tiempo (s)')
ylabel('Número de mensajes')
grid on
tiempo_medio=mean(dif_time);
moda=mode(dif_time);
desv=std(dif_time);
text(40,100,strcat("Moda= ",num2str(moda),"s"))
text(40,80,strcat("Media= ",num2str(tiempo_medio),"s"))
text(40,60,strcat("Desviación estandar= ",num2str(desv),"s"))

