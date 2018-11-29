in0 :: FromDevice(eth0);
out0 :: ToDevice(eth0);

in1 :: FromDevice(eth1);
out1 :: ToDevice(eth1);

in2 :: FromDevice(eth2);
out2 :: ToDevice(eth2);


in0out1 :: Queue;
in0out2 :: Queue;

in12out0 :: Queue;

//ARP (12/0806) AND IPv4 (12/0800) PACKETS ONLY
cw :: Classifier(
    12/0806,
    12/0800,
    -
);

//HTTP/S PACKETS ONLY
f :: IPClassifier(
	dst tcp port 80, 
	dst tcp port 443,
	-  
);

in0 -> cw;
cw[0] -> CheckARPHeader(14) -> in0out1 -> out1;  		//ARP
cw[1] -> CheckIPHeader(14) -> f;       		 	 	//IPv4
cw[2] -> Discard();			 	 		//OTHER

f[0] -> in0out1 -> out1;		 	 		//HTTP
f[1] -> in0out2 -> out2;					//HTTPS
f[2] -> Discard();						//OTHER

in1 -> in12out0 -> out0;					//IPv4 HTTP + ARP
in2 -> in12out0 -> out0;					//IPv4 HTTPS
