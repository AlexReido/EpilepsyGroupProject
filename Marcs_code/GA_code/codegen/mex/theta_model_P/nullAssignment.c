/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * nullAssignment.c
 *
 * Code generation for function 'nullAssignment'
 *
 */

/* Include files */
#include "nullAssignment.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include "theta_model_P_emxutil.h"

/* Variable Definitions */
static emlrtRTEInfo f_emlrtRTEI = { 298,/* lineNo */
  1,                                   /* colNo */
  "delete_rows",                       /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pName */
};

static emlrtRTEInfo o_emlrtRTEI = { 284,/* lineNo */
  9,                                   /* colNo */
  "nullAssignment",                    /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pName */
};

static emlrtRTEInfo p_emlrtRTEI = { 299,/* lineNo */
  5,                                   /* colNo */
  "nullAssignment",                    /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pName */
};

static emlrtRTEInfo q_emlrtRTEI = { 282,/* lineNo */
  9,                                   /* colNo */
  "nullAssignment",                    /* fName */
  "C:\\Program Files\\MATLAB\\R2020a\\toolbox\\eml\\eml\\+coder\\+internal\\nullAssignment.m"/* pName */
};

/* Function Definitions */
void delete_rows(const emlrtStack *sp, emxArray_real_T *x, const
                 emxArray_int32_T *idx)
{
  int32_T nrowx;
  emxArray_boolean_T *b;
  int32_T nrows;
  int32_T i;
  int32_T b_i;
  int32_T k;
  emxArray_real_T *b_x;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);
  nrowx = x->size[0];
  if (idx->size[1] == 1) {
    nrows = x->size[0] - 1;
    i = idx->data[0];
    for (b_i = i; b_i <= nrows; b_i++) {
      x->data[b_i - 1] = x->data[b_i];
    }

    for (b_i = i; b_i <= nrows; b_i++) {
      x->data[(b_i + x->size[0]) - 1] = x->data[b_i + x->size[0]];
    }
  } else {
    emxInit_boolean_T(sp, &b, 2, &q_emlrtRTEI, true);
    i = b->size[0] * b->size[1];
    b->size[0] = 1;
    b->size[1] = x->size[0];
    emxEnsureCapacity_boolean_T(sp, b, i, &o_emlrtRTEI);
    nrows = x->size[0];
    for (i = 0; i < nrows; i++) {
      b->data[i] = false;
    }

    i = idx->size[1];
    for (k = 0; k < i; k++) {
      b->data[idx->data[k] - 1] = true;
    }

    nrows = 0;
    i = b->size[1];
    for (k = 0; k < i; k++) {
      nrows += b->data[k];
    }

    nrows = x->size[0] - nrows;
    b_i = 0;
    for (k = 0; k < nrowx; k++) {
      if ((k + 1 > b->size[1]) || (!b->data[k])) {
        x->data[b_i] = x->data[k];
        x->data[b_i + x->size[0]] = x->data[k + x->size[0]];
        b_i++;
      }
    }

    emxFree_boolean_T(&b);
  }

  if (nrows > nrowx) {
    emlrtErrorWithMessageIdR2018a(sp, &f_emlrtRTEI,
      "Coder:builtins:AssertionFailed", "Coder:builtins:AssertionFailed", 0);
  }

  emxInit_real_T(sp, &b_x, 2, &p_emlrtRTEI, true);
  if (1 > nrows) {
    nrows = 0;
  }

  i = b_x->size[0] * b_x->size[1];
  b_x->size[0] = nrows;
  b_x->size[1] = 2;
  emxEnsureCapacity_real_T(sp, b_x, i, &p_emlrtRTEI);
  for (i = 0; i < nrows; i++) {
    b_x->data[i] = x->data[i];
  }

  for (i = 0; i < nrows; i++) {
    b_x->data[i + b_x->size[0]] = x->data[i + x->size[0]];
  }

  i = x->size[0] * x->size[1];
  x->size[0] = b_x->size[0];
  x->size[1] = 2;
  emxEnsureCapacity_real_T(sp, x, i, &p_emlrtRTEI);
  nrows = b_x->size[0];
  for (i = 0; i < nrows; i++) {
    x->data[i] = b_x->data[i];
  }

  for (i = 0; i < nrows; i++) {
    x->data[i + x->size[0]] = b_x->data[i + b_x->size[0]];
  }

  emxFree_real_T(&b_x);
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

/* End of code generation (nullAssignment.c) */
