################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
RCCarControl_2802xAdcSoc.obj: ../RCCarControl_2802xAdcSoc.c $(GEN_OPTS) $(GEN_SRCS)
	@echo 'Building file: $<'
	@echo 'Invoking: C2000 Compiler'
	"C:/ti/ccsv5/tools/compiler/c2000_6.1.3/bin/cl2000" -v28 -ml -mt -g --include_path="C:/ti/ccsv5/tools/compiler/c2000_6.1.3/include" --include_path="/packages/ti/xdais" --include_path="C:/ti/controlSUITE_06_28_2013/device_support/f2802x/v210" --include_path="C:/ti/controlSUITE_06_28_2013/libs/math/IQmath/v15c/include" --define="_DEBUG" --define="LARGE_MODEL" --quiet --verbose_diagnostics --diag_warning=225 --output_all_syms --cdebug_asm_data --preproc_with_compile --preproc_dependency="RCCarControl_2802xAdcSoc.pp" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '


