// Adder DUT
module test (
	input [3:0] A,
	input [3:0] B,
	input		clock,
	input		resetn,
	output [4:0] X
);

reg [3:0]	reg_a, reg_b;

always @(posedge clock or negedge resetn) begin
	if(~resetn) begin
		reg_a <= 4'd0;
		reg_b <= 4'd0;
	end
	else begin
		reg_a <= A;
		reg_b <= B;
	end
end

assign X = reg_a + reg_b;


  // Dump waves
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, test);
  end
endmodule
