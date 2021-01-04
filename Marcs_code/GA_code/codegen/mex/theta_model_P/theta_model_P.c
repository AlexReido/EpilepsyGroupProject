/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * theta_model_P.c
 *
 * Code generation for function 'theta_model_P'
 *
 */

/* Include files */
#include "theta_model_P.h"
#include "indexShapeCheck.h"
#include "mtimes.h"
#include "mwmathutil.h"
#include "nullAssignment.h"
#include "randn.h"
#include "rt_nonfinite.h"
#include "theta_model_P_data.h"
#include "theta_model_P_emxutil.h"
#include <string.h>

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 40,    /* lineNo */
  "theta_model_P",                     /* fcnName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pathName */
};

static emlrtRSInfo b_emlrtRSI = { 45,  /* lineNo */
  "theta_model_P",                     /* fcnName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pathName */
};

static emlrtRSInfo c_emlrtRSI = { 54,  /* lineNo */
  "theta_model_P",                     /* fcnName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pathName */
};

static emlrtRSInfo d_emlrtRSI = { 69,  /* lineNo */
  "theta_model_P",                     /* fcnName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pathName */
};

static emlrtRSInfo e_emlrtRSI = { 78,  /* lineNo */
  "theta_model_P",                     /* fcnName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pathName */
};

static emlrtRSInfo f_emlrtRSI = { 79,  /* lineNo */
  "eml_mtimes_helper",                 /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\ops\\eml_mtimes_helper.m"/* pathName */
};

static emlrtRSInfo g_emlrtRSI = { 48,  /* lineNo */
  "eml_mtimes_helper",                 /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\ops\\eml_mtimes_helper.m"/* pathName */
};

static emlrtRSInfo j_emlrtRSI = { 41,  /* lineNo */
  "find",                              /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elmat\\find.m"/* pathName */
};

static emlrtRSInfo k_emlrtRSI = { 153, /* lineNo */
  "eml_find",                          /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elmat\\find.m"/* pathName */
};

static emlrtRSInfo n_emlrtRSI = { 22,  /* lineNo */
  "nullAssignment",                    /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pathName */
};

static emlrtRSInfo o_emlrtRSI = { 26,  /* lineNo */
  "nullAssignment",                    /* fcnName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pathName */
};

static emlrtECInfo emlrtECI = { -1,    /* nDims */
  45,                                  /* lineNo */
  9,                                   /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtECInfo b_emlrtECI = { -1,  /* nDims */
  47,                                  /* lineNo */
  5,                                   /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtECInfo c_emlrtECI = { -1,  /* nDims */
  48,                                  /* lineNo */
  5,                                   /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtBCInfo emlrtBCI = { -1,    /* iFirst */
  -1,                                  /* iLast */
  54,                                  /* lineNo */
  20,                                  /* colNo */
  "x",                                 /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtRTEInfo emlrtRTEI = { 20,  /* lineNo */
  15,                                  /* colNo */
  "rdivide_helper",                    /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\rdivide_helper.m"/* pName */
};

static emlrtRTEInfo c_emlrtRTEI = { 123,/* lineNo */
  23,                                  /* colNo */
  "dynamic_size_checks",               /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\ops\\eml_mtimes_helper.m"/* pName */
};

static emlrtRTEInfo d_emlrtRTEI = { 118,/* lineNo */
  23,                                  /* colNo */
  "dynamic_size_checks",               /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\ops\\eml_mtimes_helper.m"/* pName */
};

static emlrtRTEInfo e_emlrtRTEI = { 81,/* lineNo */
  27,                                  /* colNo */
  "validate_inputs",                   /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pName */
};

static emlrtBCInfo b_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  56,                                  /* lineNo */
  9,                                   /* colNo */
  "BNI",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo c_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  68,                                  /* lineNo */
  30,                                  /* colNo */
  "aux",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo d_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  68,                                  /* lineNo */
  9,                                   /* colNo */
  "seizure_index",                     /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo e_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  62,                                  /* lineNo */
  16,                                  /* colNo */
  "aux",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo f_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  62,                                  /* lineNo */
  23,                                  /* colNo */
  "aux",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo g_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  63,                                  /* lineNo */
  38,                                  /* colNo */
  "aux",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo h_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  63,                                  /* lineNo */
  17,                                  /* colNo */
  "seizure_index",                     /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo i_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  65,                                  /* lineNo */
  38,                                  /* colNo */
  "aux",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo j_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  65,                                  /* lineNo */
  17,                                  /* colNo */
  "seizure_index",                     /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo k_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  72,                                  /* lineNo */
  41,                                  /* colNo */
  "seizure_index",                     /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo l_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  72,                                  /* lineNo */
  60,                                  /* colNo */
  "seizure_index",                     /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtBCInfo m_emlrtBCI = { -1,  /* iFirst */
  -1,                                  /* iLast */
  74,                                  /* lineNo */
  9,                                   /* colNo */
  "BNI",                               /* aName */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m",/* pName */
  0                                    /* checkKind */
};

static emlrtRTEInfo g_emlrtRTEI = { 31,/* lineNo */
  1,                                   /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtRTEInfo h_emlrtRTEI = { 39,/* lineNo */
  1,                                   /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtRTEInfo i_emlrtRTEI = { 153,/* lineNo */
  13,                                  /* colNo */
  "find",                              /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elmat\\find.m"/* pName */
};

static emlrtRTEInfo j_emlrtRTEI = { 41,/* lineNo */
  5,                                   /* colNo */
  "find",                              /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elmat\\find.m"/* pName */
};

static emlrtRTEInfo k_emlrtRTEI = { 58,/* lineNo */
  9,                                   /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtRTEInfo l_emlrtRTEI = { 69,/* lineNo */
  23,                                  /* colNo */
  "theta_model_P",                     /* fName */
  "C:\\Users\\Luke\\Documents\\Computer Science\\Year 4\\Group Project\\EpilepsyGroupProject\\Marcs_code\\GA_code\\theta_model_P.m"/* pName */
};

static emlrtRTEInfo m_emlrtRTEI = { 33,/* lineNo */
  6,                                   /* colNo */
  "find",                              /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\lib\\matlab\\elmat\\find.m"/* pName */
};

/* Function Definitions */
real_T theta_model_P(const emlrtStack *sp, const emxArray_real_T *net, real_T w,
                     real_T nodes_resected)
{
  real_T BNI;
  int32_T nx;
  emxArray_real_T *wnet;
  int32_T i;
  real_T time_seizure;
  int32_T loop_ub;
  real_T BNI_data[130];
  emxArray_boolean_T *x;
  real_T signal_data[130];
  uint8_T varargin_1[2];
  real_T theta_s_data[130];
  uint8_T varargin_2[2];
  boolean_T p;
  int32_T k;
  boolean_T exitg1;
  boolean_T b_p;
  real_T theta_old_data[130];
  int32_T x_size[1];
  int32_T tmp_size[2];
  int32_T idx;
  real_T I_data[130];
  int32_T I_size[1];
  emxArray_real_T *seizure_index;
  emxArray_int32_T *ii;
  emxArray_int32_T *b_idx;
  int32_T node;
  real_T x_tmp_data[130];
  real_T x_data[130];
  real_T tmp_data[130];
  int32_T i1;
  int32_T b_BNI[2];
  boolean_T b_tmp_data[130];
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);

  /* This function calculates BNI. This function is slightely modified from the */
  /* function theta_model (Marinho Lopes-group methods) */
  /*  version:1, Petroula Laiou,  06/01/2018 */
  /* INPUT:  */
  /*  -net            : connectivity matrix NxN  */
  /*  -w              : global coupling (scalar) */
  /*  -nodes_resected : the number of nodes that are resected */
  /* OUTPUT: */
  /*  -BNI            : BNI of the network */
  /* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */
  /* rng('shuffle');it is not supported for the convertion to the mex files */
  /*  Fixed parameters: */
  /*  time steps */
  /*  distance to SNIC */
  /*  noise level */
  /*  time step for the integration */
  /*  threshold for BNI */
  /*  window for BNI */
  if ((net->size[0] == 0) || (net->size[1] == 0)) {
    nx = 0;
  } else {
    nx = muIntScalarMax_sint32(net->size[0], net->size[1]);
  }

  /*  number of nodes */
  emxInit_real_T(sp, &wnet, 2, &g_emlrtRTEI, true);

  /*  normalisation of coupling */
  i = wnet->size[0] * wnet->size[1];
  wnet->size[0] = net->size[0];
  wnet->size[1] = net->size[1];
  emxEnsureCapacity_real_T(sp, wnet, i, &g_emlrtRTEI);
  time_seizure = (real_T)nx + nodes_resected;
  loop_ub = net->size[0] * net->size[1];
  for (i = 0; i < loop_ub; i++) {
    wnet->data[i] = w * net->data[i] / time_seizure;
  }

  /* allocate matrices and set the values of the theta model for the integration */
  /* with Euler-Maruyama */
  if (0 <= nx - 1) {
    memset(&BNI_data[0], 0, nx * sizeof(real_T));
    memset(&signal_data[0], 0, nx * sizeof(real_T));
  }

  emxInit_boolean_T(sp, &x, 2, &h_emlrtRTEI, true);
  i = x->size[0] * x->size[1];
  x->size[0] = 4000000;
  x->size[1] = nx;
  emxEnsureCapacity_boolean_T(sp, x, i, &h_emlrtRTEI);
  loop_ub = 4000000 * nx;
  for (i = 0; i < loop_ub; i++) {
    x->data[i] = false;
  }

  st.site = &emlrtRSI;
  for (i = 0; i < nx; i++) {
    theta_s_data[i] = -0.19999999999999996;
  }

  varargin_1[0] = (uint8_T)nx;
  varargin_1[1] = 1U;
  varargin_2[0] = (uint8_T)nx;
  varargin_2[1] = 1U;
  p = true;
  k = 0;
  exitg1 = false;
  while ((!exitg1) && (k < 2)) {
    if (varargin_1[k] != varargin_2[k]) {
      p = false;
      exitg1 = true;
    } else {
      k++;
    }
  }

  b_p = (int32_T)p;
  if (!b_p) {
    emlrtErrorWithMessageIdR2018a(&st, &emlrtRTEI, "MATLAB:dimagree",
      "MATLAB:dimagree", 0);
  }

  for (i = 0; i < nx; i++) {
    theta_s_data[i] /= 2.2;
  }

  st.site = &emlrtRSI;
  for (k = 0; k < nx; k++) {
    theta_s_data[k] = muDoubleScalarAcos(theta_s_data[k]);
  }

  for (i = 0; i < nx; i++) {
    theta_s_data[i] = -theta_s_data[i];
  }

  /*  stable point if I_0 < 0 */
  if (0 <= nx - 1) {
    memcpy(&theta_old_data[0], &theta_s_data[0], nx * sizeof(real_T));
  }

  /*  initial condition   */
  /*  Compute time series */
  x_size[0] = nx;
  tmp_size[0] = 1;
  tmp_size[1] = nx;
  for (idx = 0; idx < 3999999; idx++) {
    st.site = &b_emlrtRSI;
    randn(nx, I_data, I_size);
    loop_ub = I_size[0];
    for (i = 0; i < loop_ub; i++) {
      I_data[i] *= 6.0000000000000009;
    }

    if (nx != I_size[0]) {
      emlrtSizeEqCheck1DR2012b(nx, I_size[0], &emlrtECI, sp);
    }

    st.site = &b_emlrtRSI;
    for (i = 0; i < nx; i++) {
      x_tmp_data[i] = theta_old_data[i] - theta_s_data[i];
    }

    if (0 <= nx - 1) {
      memcpy(&x_data[0], &x_tmp_data[0], nx * sizeof(real_T));
    }

    for (k = 0; k < nx; k++) {
      x_data[k] = muDoubleScalarCos(x_data[k]);
    }

    for (i = 0; i < nx; i++) {
      x_data[i] = 1.0 - x_data[i];
    }

    b_st.site = &g_emlrtRSI;
    if (wnet->size[0] != nx) {
      if (((wnet->size[0] == 1) && (wnet->size[1] == 1)) || (nx == 1)) {
        emlrtErrorWithMessageIdR2018a(&b_st, &d_emlrtRTEI,
          "Coder:toolbox:mtimes_noDynamicScalarExpansion",
          "Coder:toolbox:mtimes_noDynamicScalarExpansion", 0);
      } else {
        emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI, "MATLAB:innerdim",
          "MATLAB:innerdim", 0);
      }
    }

    b_st.site = &f_emlrtRSI;
    mtimes(wnet, x_data, x_size, tmp_data, I_size);
    if (nx != I_size[0]) {
      emlrtSizeEqCheck1DR2012b(nx, I_size[0], &emlrtECI, sp);
    }

    for (i = 0; i < nx; i++) {
      I_data[i] = (-1.2 + I_data[i]) + tmp_data[i];
    }

    for (k = 0; k < nx; k++) {
      tmp_data[k] = muDoubleScalarCos(theta_old_data[k]);
    }

    for (i = 0; i < nx; i++) {
      I_data[i] *= tmp_data[i] + 1.0;
    }

    for (i = 0; i < nx; i++) {
      tmp_data[i] = 0.01 * ((1.0 - tmp_data[i]) + I_data[i]);
    }

    for (k = 0; k < nx; k++) {
      x_tmp_data[k] = muDoubleScalarCos(x_tmp_data[k]);
    }

    for (i = 0; i < nx; i++) {
      x_tmp_data[i] = 0.5 * (1.0 - x_tmp_data[i]);
    }

    b_BNI[0] = 1;
    b_BNI[1] = nx;
    emlrtSubAssignSizeCheckR2012b(&b_BNI[0], 2, &nx, 1, &b_emlrtECI, sp);
    if (0 <= nx - 1) {
      memcpy(&signal_data[0], &x_tmp_data[0], nx * sizeof(real_T));
    }

    for (i = 0; i < nx; i++) {
      b_tmp_data[i] = (signal_data[i] > 0.9);
    }

    b_BNI[0] = 1;
    b_BNI[1] = x->size[1];
    emlrtSubAssignSizeCheckR2012b(&b_BNI[0], 2, &tmp_size[0], 2, &c_emlrtECI, sp);
    for (i = 0; i < nx; i++) {
      x->data[(idx + 4000000 * i) + 1] = b_tmp_data[i];
    }

    for (i = 0; i < nx; i++) {
      theta_old_data[i] += tmp_data[i];
    }

    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  emxFree_real_T(&wnet);

  /*  Compute BNI */
  emxInit_real_T(sp, &seizure_index, 2, &k_emlrtRTEI, true);
  emxInit_int32_T(sp, &ii, 1, &m_emlrtRTEI, true);
  emxInit_int32_T(sp, &b_idx, 2, &l_emlrtRTEI, true);
  for (node = 0; node < nx; node++) {
    st.site = &c_emlrtRSI;
    i = node + 1;
    if ((i < 1) || (i > x->size[1])) {
      emlrtDynamicBoundsCheckR2012b(i, 1, x->size[1], &emlrtBCI, &st);
    }

    b_st.site = &j_emlrtRSI;
    c_st.site = &k_emlrtRSI;
    idx = 0;
    i = ii->size[0];
    ii->size[0] = 4000000;
    emxEnsureCapacity_int32_T(&c_st, ii, i, &i_emlrtRTEI);
    loop_ub = 0;
    exitg1 = false;
    while ((!exitg1) && (loop_ub < 4000000)) {
      if (x->data[loop_ub + 4000000 * node]) {
        idx++;
        ii->data[idx - 1] = loop_ub + 1;
        if (idx >= 4000000) {
          exitg1 = true;
        } else {
          loop_ub++;
        }
      } else {
        loop_ub++;
      }
    }

    if (1 > idx) {
      i = 0;
    } else {
      i = idx;
    }

    indexShapeCheck();
    i1 = ii->size[0];
    if (1 > idx) {
      ii->size[0] = 0;
    } else {
      ii->size[0] = idx;
    }

    emxEnsureCapacity_int32_T(&c_st, ii, i1, &j_emlrtRTEI);
    if (i == 0) {
      i = node + 1;
      if ((i < 1) || (i > nx)) {
        emlrtDynamicBoundsCheckR2012b(i, 1, nx, &b_emlrtBCI, sp);
      }

      BNI_data[i - 1] = 0.0;
    } else {
      i1 = seizure_index->size[0] * seizure_index->size[1];
      seizure_index->size[0] = i;
      seizure_index->size[1] = 2;
      emxEnsureCapacity_real_T(sp, seizure_index, i1, &k_emlrtRTEI);
      loop_ub = i << 1;
      for (i1 = 0; i1 < loop_ub; i1++) {
        seizure_index->data[i1] = 0.0;
      }

      seizure_index->data[0] = ii->data[0];
      k = 1;
      for (loop_ub = 0; loop_ub <= i - 2; loop_ub++) {
        i1 = loop_ub + 2;
        if ((i1 < 1) || (i1 > i)) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i, &e_emlrtBCI, sp);
        }

        idx = loop_ub + 1;
        if ((idx < 1) || (idx > i)) {
          emlrtDynamicBoundsCheckR2012b(idx, 1, i, &f_emlrtBCI, sp);
        }

        if (ii->data[i1 - 1] - ii->data[idx - 1] > 2400) {
          i1 = loop_ub + 1;
          if ((i1 < 1) || (i1 > i)) {
            emlrtDynamicBoundsCheckR2012b(i1, 1, i, &g_emlrtBCI, sp);
          }

          if (k > seizure_index->size[0]) {
            emlrtDynamicBoundsCheckR2012b(k, 1, seizure_index->size[0],
              &h_emlrtBCI, sp);
          }

          seizure_index->data[(k + seizure_index->size[0]) - 1] = ii->data[i1 -
            1];
          k++;
          i1 = loop_ub + 2;
          if ((i1 < 1) || (i1 > i)) {
            emlrtDynamicBoundsCheckR2012b(i1, 1, i, &i_emlrtBCI, sp);
          }

          if ((k < 1) || (k > seizure_index->size[0])) {
            emlrtDynamicBoundsCheckR2012b(k, 1, seizure_index->size[0],
              &j_emlrtBCI, sp);
          }

          seizure_index->data[k - 1] = ii->data[i1 - 1];
        }

        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      if (i < 1) {
        emlrtDynamicBoundsCheckR2012b(i, 1, i, &c_emlrtBCI, sp);
      }

      if (k > seizure_index->size[0]) {
        emlrtDynamicBoundsCheckR2012b(k, 1, seizure_index->size[0], &d_emlrtBCI,
          sp);
      }

      seizure_index->data[(k + seizure_index->size[0]) - 1] = ii->data[i - 1];
      st.site = &d_emlrtRSI;
      i = b_idx->size[0] * b_idx->size[1];
      b_idx->size[0] = 1;
      b_idx->size[1] = seizure_index->size[0] - k;
      emxEnsureCapacity_int32_T(&st, b_idx, i, &l_emlrtRTEI);
      loop_ub = seizure_index->size[0] - k;
      for (i = 0; i < loop_ub; i++) {
        b_idx->data[i] = (k + i) + 1;
      }

      b_st.site = &n_emlrtRSI;
      b_p = true;
      loop_ub = 0;
      exitg1 = false;
      while ((!exitg1) && (loop_ub <= (seizure_index->size[0] - k) - 1)) {
        if (b_idx->data[loop_ub] > seizure_index->size[0]) {
          b_p = false;
          exitg1 = true;
        } else {
          loop_ub++;
        }
      }

      if (!b_p) {
        emlrtErrorWithMessageIdR2018a(&b_st, &e_emlrtRTEI,
          "MATLAB:subsdeldimmismatch", "MATLAB:subsdeldimmismatch", 0);
      }

      i = b_idx->size[0] * b_idx->size[1];
      b_idx->size[0] = 1;
      b_idx->size[1] = seizure_index->size[0] - k;
      emxEnsureCapacity_int32_T(&st, b_idx, i, &l_emlrtRTEI);
      loop_ub = seizure_index->size[0] - k;
      for (i = 0; i < loop_ub; i++) {
        b_idx->data[i] = (k + i) + 1;
      }

      b_st.site = &o_emlrtRSI;
      delete_rows(&b_st, seizure_index, b_idx);
      time_seizure = 0.0;
      i = seizure_index->size[0];
      for (loop_ub = 0; loop_ub < i; loop_ub++) {
        i1 = loop_ub + 1;
        if ((i1 < 1) || (i1 > seizure_index->size[0])) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, seizure_index->size[0],
            &k_emlrtBCI, sp);
        }

        idx = loop_ub + 1;
        if ((idx < 1) || (idx > seizure_index->size[0])) {
          emlrtDynamicBoundsCheckR2012b(idx, 1, seizure_index->size[0],
            &l_emlrtBCI, sp);
        }

        time_seizure = ((time_seizure + seizure_index->data[(i1 +
          seizure_index->size[0]) - 1]) - seizure_index->data[idx - 1]) + 1.0;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      i = node + 1;
      if ((i < 1) || (i > nx)) {
        emlrtDynamicBoundsCheckR2012b(i, 1, nx, &m_emlrtBCI, sp);
      }

      BNI_data[i - 1] = time_seizure / 4.0E+6;
    }

    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  emxFree_int32_T(&b_idx);
  emxFree_int32_T(&ii);
  emxFree_real_T(&seizure_index);
  emxFree_boolean_T(&x);
  st.site = &e_emlrtRSI;
  if (nx == 0) {
    time_seizure = 0.0;
  } else {
    time_seizure = BNI_data[0];
    for (k = 2; k <= nx; k++) {
      time_seizure += BNI_data[k - 1];
    }
  }

  BNI = time_seizure / (real_T)nx;
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
  return BNI;
}

/* End of code generation (theta_model_P.c) */
