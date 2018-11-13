in0 :: FromDevice(eth0);
out0 :: ToDevice(eth0);

in1 :: FromDevice(eth1);
out1 :: ToDevice(eth1);

qin0out1 :: Queue;
qin1out0 :: Queue;

cw1::Classifier(
  12/86dd,
  -
);
cw2::Classifier(
  12/86dd,
  -
);

in0 -> cw1;
cw1[0] -> Strip(14) -> CheckIP6Header() -> IPEncap(4, 18.26.4.24, 140.247.60.147) -> qin0out1 -> out1; 	//IPv6
cw1[1] -> qin0out1 -> out1;			 					  												//OTHER

in1 -> cw2;
cw2[0] -> Strip(34) -> CheckIP6Header() -> qin1out0 -> out0; 											//IPv6
cw2[1] -> qin1out0 -> out0;			 					  												//OTHER
