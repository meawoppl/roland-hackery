Mode One Commands
=================

These are the 'mode 1' commands supported in the roland g-code dialect.

| Name | Code| Args             | Units  | Cut | Description | [Mode] After |
|:----:|:---:|----------------- |-----------------|:---:|--|:---:|
| Draw     |  D  | ($x_n$, $y_n$)*  |  10um        | X | **Cuts** from Current to **ABS** location(s)  | **ABS** |
| Feed     |  F  |  $f_{mm/s}$      |  mm/s        |   |   |
| Home     |  H  | N/A              |              |   | Move the to (0,0) user coordinate  |
|  ?       |  I  | ($x_n$, $y_n$)*  |  10um        | X | Lowers to $Z_1$ then **CUTS** relative  | **REL** |
| Tool     |  J  | $I_n$            | integer #    |   | Tool Change **(FOUND BY RE)**
| Move     |  M  | ($x_n$, $y_n$)*  |  10um        |   | Raises to $Z_2$ moves **ABS** fast | **ABS** |
| Rel Move |  R  |  ($x_n$, $y_n$)* |  10um        |   | Raises to $Z_2$, moves **REL** fast | **REL**  |
| Velocity |  V  | $v_{mm/s}$       | (float) mm/s |   | Sets the velocity for cutting moves (**D**, **I**, **Z**) |
| Dwell    |  W  | $I_{us}$         | ms           |   | Dwell for the specified number of milliseconds  |
| XYZ Move |  Z  | ($x_n$, $y_n$, $z_n$)*  | 10um  | X | Moves in **[Mode]**, speed is specified by **V** or **!VZ** command   |
| @ |   |   |   |   |
| ^ |   |   |   |   |


Hints found here:
https://forums.autodesk.com/t5/hsm-post-processor-forum/roland-rml-post-processors/td-p/6095150

