################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
startup_ccs.obj: ../startup_ccs.c $(GEN_OPTS) $(GEN_SRCS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv5/tools/compiler/arm_5.0.4/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv5/tools/compiler/arm_5.0.4/include" --include_path="C:/StellarisWare/boards/ek-lm4f120xl" --include_path="C:/StellarisWare" --gcc --define=ccs="ccs" --define=PART_LM4F120H5QR --define=TARGET_IS_BLIZZARD_RA2 --define=UART_BUFFERED --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="startup_ccs.pp" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

usb_dev_serial.obj: ../usb_dev_serial.c $(GEN_OPTS) $(GEN_SRCS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv5/tools/compiler/arm_5.0.4/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv5/tools/compiler/arm_5.0.4/include" --include_path="C:/StellarisWare/boards/ek-lm4f120xl" --include_path="C:/StellarisWare" --gcc --define=ccs="ccs" --define=PART_LM4F120H5QR --define=TARGET_IS_BLIZZARD_RA2 --define=UART_BUFFERED --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="usb_dev_serial.pp" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

usb_serial_structs.obj: ../usb_serial_structs.c $(GEN_OPTS) $(GEN_SRCS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv5/tools/compiler/arm_5.0.4/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv5/tools/compiler/arm_5.0.4/include" --include_path="C:/StellarisWare/boards/ek-lm4f120xl" --include_path="C:/StellarisWare" --gcc --define=ccs="ccs" --define=PART_LM4F120H5QR --define=TARGET_IS_BLIZZARD_RA2 --define=UART_BUFFERED --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="usb_serial_structs.pp" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '


