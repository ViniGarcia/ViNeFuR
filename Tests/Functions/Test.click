in01 :: FromDevice(eth0);
out01 :: ToDevice(eth0);

in02 :: FromDevice(eth1);
out02 :: ToDevice(eth1);

q1 :: Queue;
q2 :: Queue;

in01 -> Print("1-> ") -> q1 -> out02;
in02 -> Print("2-> ") -> q2 -> out01;
