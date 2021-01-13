/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * theta_model_P_data.c
 *
 * Code generation for function 'theta_model_P_data'
 *
 */

/* Include files */
#include "theta_model_P_data.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Variable Definitions */
emlrtCTX emlrtRootTLSGlobal = NULL;
const volatile char_T *emlrtBreakCheckR2012bFlagVar = NULL;
omp_lock_t emlrtLockGlobal;
omp_nest_lock_t emlrtNestLockGlobal;
emlrtContext emlrtContextGlobal = { true,/* bFirstTime */
  false,                               /* bInitialized */
  131594U,                             /* fVersionInfo */
  NULL,                                /* fErrorFunction */
  "theta_model_P",                     /* fFunctionName */
  NULL,                                /* fRTCallStack */
  false,                               /* bDebugMode */
  { 2045744189U, 2170104910U, 2743257031U, 4284093946U },/* fSigWrd */
  NULL                                 /* fSigMem */
};

emlrtRSInfo j_emlrtRSI = { 62,         /* lineNo */
  "applyScalarFunction",               /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"/* pathName */
};

emlrtRSInfo k_emlrtRSI = { 61,         /* lineNo */
  "scalar_erfinv",                     /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo l_emlrtRSI = { 310,        /* lineNo */
  "scalar_erfinv_and_erfcinv",         /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo m_emlrtRSI = { 314,        /* lineNo */
  "scalar_erfinv_and_erfcinv",         /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo n_emlrtRSI = { 344,        /* lineNo */
  "scalar_erfinv_and_erfcinv",         /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo o_emlrtRSI = { 355,        /* lineNo */
  "scalar_erfinv_and_erfcinv",         /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo p_emlrtRSI = { 366,        /* lineNo */
  "scalar_erfinv_and_erfcinv",         /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo q_emlrtRSI = { 15,         /* lineNo */
  "eml_erfcore",                       /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo r_emlrtRSI = { 49,         /* lineNo */
  "applyScalarFunction",               /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"/* pathName */
};

emlrtRSInfo s_emlrtRSI = { 56,         /* lineNo */
  "scalar_erfc",                       /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo t_emlrtRSI = { 236,        /* lineNo */
  "scalar_erf_and_erfc",               /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo u_emlrtRSI = { 238,        /* lineNo */
  "scalar_erf_and_erfc",               /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo v_emlrtRSI = { 17,         /* lineNo */
  "log2",                              /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elfun\\log2.m"/* pathName */
};

emlrtRSInfo w_emlrtRSI = { 47,         /* lineNo */
  "applyScalarFunction",               /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"/* pathName */
};

emlrtRSInfo x_emlrtRSI = { 17,         /* lineNo */
  "log2",                              /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\+scalar\\log2.m"/* pathName */
};

emlrtRSInfo y_emlrtRSI = { 12,         /* lineNo */
  "pow2",                              /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elfun\\pow2.m"/* pathName */
};

emlrtRSInfo ab_emlrtRSI = { 12,        /* lineNo */
  "pow2",                              /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\+scalar\\pow2.m"/* pathName */
};

emlrtRSInfo bb_emlrtRSI = { 70,        /* lineNo */
  "power",                             /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\ops\\power.m"/* pathName */
};

emlrtRSInfo cb_emlrtRSI = { 12,        /* lineNo */
  "eml_erfcore",                       /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo db_emlrtRSI = { 51,        /* lineNo */
  "scalar_erf",                        /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\specfun\\private\\eml_erfcore.m"/* pathName */
};

emlrtRSInfo gb_emlrtRSI = { 168,       /* lineNo */
  "mtimes",                            /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\+blas\\mtimes.m"/* pathName */
};

emlrtRSInfo hb_emlrtRSI = { 164,       /* lineNo */
  "mtimes",                            /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\+blas\\mtimes.m"/* pathName */
};

emlrtRSInfo kb_emlrtRSI = { 397,       /* lineNo */
  "find_first_indices",                /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elmat\\find.m"/* pathName */
};

emlrtRSInfo lb_emlrtRSI = { 43,        /* lineNo */
  "indexShapeCheck",                   /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\indexShapeCheck.m"/* pathName */
};

emlrtRTEInfo b_emlrtRTEI = { 18,       /* lineNo */
  15,                                  /* colNo */
  "mean",                              /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\datafun\\mean.m"/* pName */
};

/* End of code generation (theta_model_P_data.c) */
