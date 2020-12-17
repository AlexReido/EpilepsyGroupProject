/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * theta_model_P.h
 *
 * Code generation for function 'theta_model_P'
 *
 */

#pragma once

/* Include files */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mex.h"
#include "emlrt.h"
#include "rtwtypes.h"
#include "theta_model_P_types.h"

/* Function Declarations */
real_T theta_model_P(const emlrtStack *sp, const emxArray_real_T *net, real_T w,
                     real_T nodes_resected);

/* End of code generation (theta_model_P.h) */
