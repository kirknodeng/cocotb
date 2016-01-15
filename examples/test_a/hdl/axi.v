`define  SVT_AXI_MAX_ADDR_WIDTH                      32     //64 
`define  SVT_AXI_PROT_WIDTH                          3 
`define  SVT_AXI_CACHE_WIDTH                         4     
`define  SVT_AXI_MAX_ID_WIDTH                        8
`define  SVT_AXI_MAX_BURST_LENGTH_WIDTH              10
`define  SVT_AXI_BURST_WIDTH                         2
`define  SVT_AXI_SIZE_WIDTH                          3
`define  SVT_AXI_LOCK_WIDTH                          2
`define  SVT_AXI_MAX_DATA_WIDTH                      1024
`define  SVT_AXI_RESP_WIDTH                          4
module axi (
  //-----------------------------------------
  // AXI Signals 
  //-----------------------------------------
  // Clock and Reset signals
  input                                         i_ACLK,
  input                                         i_ARESETn,
  // AXI Protocol Interface M1 - Dataflow signals
  input  [`SVT_AXI_MAX_ADDR_WIDTH-1:0]          i_AWADDR,
  input                                         i_AWVALID,
  input  [`SVT_AXI_MAX_BURST_LENGTH_WIDTH-1:0]  i_AWLEN,
  input  [`SVT_AXI_BURST_WIDTH-1:0]             i_AWBURST,
  input  [`SVT_AXI_SIZE_WIDTH-1:0]              i_AWSIZE,
  input  [`SVT_AXI_LOCK_WIDTH-1:0]              i_AWLOCK,
  input  [`SVT_AXI_PROT_WIDTH-1:0]              i_AWPROT,
  input  [`SVT_AXI_CACHE_WIDTH-1:0]             i_AWCACHE,
  input  [`SVT_AXI_MAX_ID_WIDTH-1:0]            i_AWID,
  output                                        i_AWREADY,

  input  [`SVT_AXI_MAX_ADDR_WIDTH-1:0]          i_ARADDR,
  input                                         i_ARVALID,
  input  [`SVT_AXI_MAX_BURST_LENGTH_WIDTH-1:0]  i_ARLEN,
  input  [`SVT_AXI_BURST_WIDTH-1:0]             i_ARBURST,
  input  [`SVT_AXI_SIZE_WIDTH-1:0]              i_ARSIZE,
  input  [`SVT_AXI_LOCK_WIDTH-1:0]              i_ARLOCK,
  input  [`SVT_AXI_PROT_WIDTH-1:0]              i_ARPROT,
  input  [`SVT_AXI_CACHE_WIDTH-1:0]             i_ARCACHE,
  input  [`SVT_AXI_MAX_ID_WIDTH-1:0]            i_ARID,
  input                                         i_ARREADY,

  input  [`SVT_AXI_MAX_DATA_WIDTH-1:0]          i_WDATA,
  input                                         i_WVALID,
  input  [`SVT_AXI_MAX_DATA_WIDTH/8-1:0]        i_WSTRB,
  input                                         i_WLAST,
  input  [`SVT_AXI_MAX_ID_WIDTH-1:0]            i_WID,
  output										i_WREADY,

  input [`SVT_AXI_MAX_DATA_WIDTH-1:0]           i_RDATA,
  input                                         i_RVALID,
  input                                         i_RLAST,
  input [`SVT_AXI_RESP_WIDTH-1:0]               i_RRESP,
  input [`SVT_AXI_MAX_ID_WIDTH-1:0]             i_RID,
  input                                         i_RREADY,

  output[`SVT_AXI_RESP_WIDTH-1:0]               i_BRESP,
  output                                         i_BVALID,
  input [`SVT_AXI_MAX_ID_WIDTH-1:0]             i_BID,
  input                                         i_BREADY
  );
  assign i_AWREADY = 1'b1;
  assign i_WREADY = 1'b1;
  assign i_BRESP = 1'b0;
  assign i_BVALID = 1'b1;

  // Dump waves
  initial begin
    $dumpfile("axi4_dump.vcd");
    $dumpvars(1, axi);
  end
  endmodule
