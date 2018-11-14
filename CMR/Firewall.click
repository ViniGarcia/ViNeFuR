in0 :: FromDevice(eth0);
out0 :: ToDevice(eth0);

in1 :: FromDevice(eth1);
out1 :: ToDevice(eth1);

in0out1 :: Queue;
in1out0 :: Queue;

//ARP (12/0806), IPv4 (12/0800) AND IPv6 (12/86dd) PACKETS ONLY
cw :: Classifier(
    12/0806,
    12/0800,
    12/86dd,
    -
);

//HTTP/S PACKETS ONLY
f :: IPClassifier(
	dst tcp port 80 or 443,
	-  
);

in0 -> cw;
cw[0] -> CheckARPHeader(14) -> in0out1 -> out1;  		//ARP
cw[1] -> CheckIPHeader(14) -> f;       		 	 	//IPv4
cw[2] -> Strip(14) -> CheckIP6Header() -> Print() -> f;		//IPv6
cw[3] -> Discard();			 			//OTHER

f[0] -> in0out1 -> out1;		 			//HTTP/S
f[1] -> Discard();			 			//OTHER

in1 -> in1out0 -> out0; 					//RETURN
