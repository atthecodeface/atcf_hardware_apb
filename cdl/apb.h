/** Copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @file   apb.h
 * @brief  Types for the APB bus
 *
 * Header file for the types for an APB bus, but no modules
 *
 */

/*a Types */
/*t t_apb_request */
typedef struct {
    bit[32] paddr;
    bit     penable;
    bit     psel;
    bit     pwrite;
    bit[32] pwdata;
} t_apb_request;

/*t t_apb_response */
typedef struct {
    bit[32] prdata;
    bit     pready;
    bit     perr;
} t_apb_response;

/*t t_apb_processor_response */
typedef struct {
    bit acknowledge;
    bit rom_busy;
} t_apb_processor_response;

/*t t_apb_processor_request */
typedef struct {
    bit valid;
    bit[16] address;
} t_apb_processor_request;

/*t t_apb_rom_request */
typedef struct {
    bit enable;
    bit[16] address;
} t_apb_rom_request;

/*t t_apb_script_master_op
  The protocol is:

  idle +
  (start | start_clear)
  { idle *
    data } *
  idle *
  (data_last)
  idle +
  
The state machine will error if data_last and the number of data valid
does not provide a complete operation; hence it can be aborted if
data_last and 0 data are valid.
 */
typedef enum[3] {
    asm_op_idle,
    asm_op_start,
    asm_op_start_clear,
    asm_op_data,
    asm_op_data_last,
} t_apb_script_master_op;

/*t t_apb_script_master_resp_type */
typedef enum[3] {
    asm_resp_idle,
    asm_resp_running,
    asm_resp_completed,
    asm_resp_poll_failed,
    asm_resp_errored
} t_apb_script_master_resp_type;

/*t t_apb_script_master_request */
typedef struct {
    t_apb_script_master_op op;
    bit[3] num_data_valid "Number of bytes valid, 0 to 6, in data; ignored if not an op data";
    bit[48] data;
} t_apb_script_master_request;

/*t t_apb_script_master_response
  The protocol is:

  idle +
  running +
  completing *
  (completed | poll_failed | errored)
  idle +
  
 */
typedef struct {
    t_apb_script_master_resp_type resp_type;
    bit[3] bytes_consumed "If non-zero then remove the bottom bytes from the data request in the next cycle; data is never consumed in back-to-back cycles, and this will be zero for one cycle after it is nonzero";
    bit[2] bytes_valid; // 1, 2, or 3 for 32-bit
    bit[32] data;
} t_apb_script_master_response;

