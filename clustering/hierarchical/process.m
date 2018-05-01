clear all
close all
clc

%% read csv file with tweets and 6 dimensions

%filename = 'election/data_election/election_crysmile.csv';
filename = 'efcrysmile/efcrysmile_6d_mod.csv';

M = csvread(filename);

%% https://www.mathworks.com/help/fuzzy/fcm.html#buwj13j
% k-means clustering

[centers,U] = fcm(M,20);

maxU = max(U);
index1 = find(U(1,:) == maxU);
index2 = find(U(2,:) == maxU);

plot(M(index1,1),M(index1,2),'ob')
hold on
plot(M(index2,1),M(index2,2),'or')
plot(centers(1,1),centers(1,2),'xb','MarkerSize',15,'LineWidth',3)
plot(centers(2,1),centers(2,2),'xr','MarkerSize',15,'LineWidth',3)
hold off

%% hierarchical clustering
% https://www.mathworks.com/help/stats/hierarchical-clustering.html

Y=pdist(M);
Z=linkage(Y,'average');
%dendrogram(Z)
%c = cophenet(Z,Y) %for efcrysmile_6d c=0.5484

%out of memory
%leafOrder = optimalleaforder(Z,Y);%https://www.mathworks.com/help/stats/optimalleaforder.html
%dendrogram(Z,'reorder',leafOrder)

[~,T] = dendrogram(Z,'ColorThreshold','default');%define node number dfault 30, and list all nodes

%% Find tweets correspond to cluster node and boxplot 6-d emotion for a cluster
a1=find(T==1);%get all data points for the first cluster
a2=find(T==2);
a3=find(T==3);
a4=find(T==5);
a5=find(T==17);
a6=find(T==23);
a7=find(T==24);
a8=find(T==21);
a9=find(T==29);
%a10=find(T==23);


c=vertcat(a1,a2,a3,a4,a5,a6,a7,a8,a9);

c=sort(c);
results=M(c,:);
boxplot(results);

%%





