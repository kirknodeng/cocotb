// Adder DUT
module test (input [3:0] A,
              input [3:0] B,
              output reg [4:0] X);
  always @(A or B) begin
    X = A + B;
  end

  // Dump waves
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, test);
  end
//  initial begin
//	$fsdbDumpfile("./tbench.fsdb");
//	$fsdbDumpvars;
//  end

endmodule
