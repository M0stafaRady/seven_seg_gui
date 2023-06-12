`timescale  1ns/1ps
`define     SIM_LIMIT   100_000_000

module timer_tb;
    reg clk;
    reg rst;
    wire [7:0]  seven_seg;
    wire [3:0]  digit_en;  
    timer uut (
        .clk(clk),
        .rst(rst),
        .seven_seg(seven_seg),
        .digit_en(digit_en)
    );

    initial begin
        $dumpfile("timer_tb.vcd");
        $dumpvars;
        #`SIM_LIMIT $finish;  
    end

    initial begin
        clk <= 1'b0;
        rst <= 1'b0;
        #100;
        rst <= 1'b1;
        #999;
        @(posedge clk) rst <= 0;
    end

endmodule