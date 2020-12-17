/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * mtimes.c
 *
 * Code generation for function 'mtimes'
 *
 */

/* Include files */
#include "mtimes.h"
#include "blas.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include <string.h>

/* Function Definitions */
void mtimes(const emxArray_real_T *A, const real_T B_data[], const int32_T
            B_size[1], real_T C_data[], int32_T C_size[1])
{
  int32_T loop_ub;
  char_T TRANSB1;
  char_T TRANSA1;
  real_T alpha1;
  real_T beta1;
  ptrdiff_t m_t;
  ptrdiff_t n_t;
  ptrdiff_t k_t;
  ptrdiff_t lda_t;
  ptrdiff_t ldb_t;
  ptrdiff_t ldc_t;
  if ((A->size[0] == 0) || (A->size[1] == 0) || (B_size[0] == 0)) {
    C_size[0] = A->size[1];
    loop_ub = A->size[1];
    if (0 <= loop_ub - 1) {
      memset(&C_data[0], 0, loop_ub * sizeof(real_T));
    }
  } else {
    TRANSB1 = 'N';
    TRANSA1 = 'T';
    alpha1 = 1.0;
    beta1 = 0.0;
    m_t = (ptrdiff_t)A->size[1];
    n_t = (ptrdiff_t)1;
    k_t = (ptrdiff_t)A->size[0];
    lda_t = (ptrdiff_t)A->size[0];
    ldb_t = (ptrdiff_t)B_size[0];
    ldc_t = (ptrdiff_t)A->size[1];
    C_size[0] = A->size[1];
    dgemm(&TRANSA1, &TRANSB1, &m_t, &n_t, &k_t, &alpha1, &A->data[0], &lda_t,
          &B_data[0], &ldb_t, &beta1, &C_data[0], &ldc_t);
  }
}

/* End of code generation (mtimes.c) */
