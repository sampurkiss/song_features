song_features = csvread("song_details.csv");





%%%%%%%%%%%

%Filter out data
%remove any with all zero values
X = song_features(sum(song_features,axis=2)>0,:);
X = X(!any(isnan(X),2),:);


%normalize features
#X = (song_features - mean(song_features))./std(song_features);

mu = mean(X)

%p_x = pi*(1/sqrt(


