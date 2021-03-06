/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * applyScalarFunction.c
 *
 * Code generation for function 'applyScalarFunction'
 *
 */

/* Include files */
#include "applyScalarFunction.h"
#include "log2.h"
#include "mwmathutil.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Function Declarations */
static real_T eml_erfcore(real_T x);

/* Function Definitions */
static real_T eml_erfcore(real_T x)
{
  real_T y;
  real_T absx;
  real_T P;
  real_T s;
  real_T R;
  real_T S;

  /* ========================== COPYRIGHT NOTICE ============================ */
  /*  The algorithms for calculating ERF(X) and ERFC(X) are derived           */
  /*  from FDLIBM, which has the following notice:                            */
  /*                                                                          */
  /*  Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.       */
  /*                                                                          */
  /*  Developed at SunSoft, a Sun Microsystems, Inc. business.                */
  /*  Permission to use, copy, modify, and distribute this                    */
  /*  software is freely granted, provided that this notice                   */
  /*  is preserved.                                                           */
  /* =============================    END    ================================ */
  absx = muDoubleScalarAbs(x);
  if (muDoubleScalarIsNaN(x)) {
    y = x;
  } else if (muDoubleScalarIsInf(x)) {
    if (x < 0.0) {
      y = 2.0;
    } else {
      y = 0.0;
    }
  } else if (absx < 0.84375) {
    if (absx < 1.3877787807814457E-17) {
      y = 1.0 - x;
    } else {
      s = x * x;
      y = (s * (s * (s * (s * -2.3763016656650163E-5 + -0.0057702702964894416) +
                     -0.02848174957559851) + -0.3250421072470015) +
           0.12837916709551256) / (s * (s * (s * (s * (s *
        -3.9602282787753681E-6 + 0.00013249473800432164) + 0.0050813062818757656)
        + 0.0650222499887673) + 0.39791722395915535) + 1.0);
      if (x < 0.25) {
        y = 1.0 - (x + x * y);
      } else {
        y = 0.5 - (x * y + (x - 0.5));
      }
    }
  } else if (absx < 1.25) {
    P = (absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx -
      1.0) * ((absx - 1.0) * -0.0021663755948687908 + 0.035478304325618236) +
      -0.11089469428239668) + 0.31834661990116175) + -0.37220787603570132) +
                        0.41485611868374833) + -0.0023621185607526594;
    s = (absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx -
      1.0) * ((absx - 1.0) * 0.011984499846799107 + 0.013637083912029051) +
      0.12617121980876164) + 0.071828654414196266) + 0.540397917702171) +
                        0.10642088040084423) + 1.0;
    if (x >= 0.0) {
      y = 0.15493708848953247 - P / s;
    } else {
      y = (P / s + 0.84506291151046753) + 1.0;
    }
  } else if (x < -6.0) {
    y = 2.0;
  } else if (x >= 28.0) {
    y = 0.0;
  } else {
    s = 1.0 / (absx * absx);
    if (absx < 2.8571414947509766) {
      R = s * (s * (s * (s * (s * (s * (s * -9.8143293441691455 +
        -81.2874355063066) + -184.60509290671104) + -162.39666946257347) +
                         -62.375332450326006) + -10.558626225323291) +
               -0.69385857270718176) + -0.0098649440348471482;
      S = s * (s * (s * (s * (s * (s * (s * (s * -0.0604244152148581 +
        6.5702497703192817) + 108.63500554177944) + 429.00814002756783) +
                  645.38727173326788) + 434.56587747522923) + 137.65775414351904)
               + 19.651271667439257) + 1.0;
    } else {
      R = s * (s * (s * (s * (s * (s * -483.5191916086514 + -1025.0951316110772)
                  + -637.56644336838963) + -160.63638485582192) +
                    -17.757954917754752) + -0.799283237680523) +
        -0.0098649429247001;
      S = s * (s * (s * (s * (s * (s * (s * -22.440952446585818 +
        474.52854120695537) + 2553.0504064331644) + 3199.8582195085955) +
                         1536.729586084437) + 325.79251299657392) +
               30.338060743482458) + 1.0;
    }

    b_log2(absx, &s, &P);
    s = muDoubleScalarFloor(s * 2.097152E+6) / 2.097152E+6 * muDoubleScalarPower
      (2.0, P);
    y = muDoubleScalarExp(-s * s - 0.5625) * muDoubleScalarExp((s - absx) * (s +
      absx) + R / S) / absx;
    if (x < 0.0) {
      y = 2.0 - y;
    }
  }

  return y;
}

void applyScalarFunction(const emlrtStack *sp, const real_T x_data[], const
  int32_T x_size[1], real_T z1_data[], int32_T z1_size[1])
{
  int32_T ub_loop;
  int32_T k;
  real_T y;
  real_T z;
  real_T absx;
  real_T P;
  real_T R;
  real_T S;
  jmp_buf * volatile emlrtJBStack;
  emlrtStack st;
  jmp_buf b_emlrtJBEnviron;
  boolean_T emlrtHadParallelError = false;
  z1_size[0] = x_size[0];
  ub_loop = x_size[0] - 1;
  emlrtEnterParallelRegion(sp, omp_in_parallel());
  emlrtPushJmpBuf(sp, &emlrtJBStack);

#pragma omp parallel \
 num_threads(emlrtAllocRegionTLSs(sp->tls, omp_in_parallel(), omp_get_max_threads(), omp_get_num_procs())) \
 private(st,b_emlrtJBEnviron,y,z,absx,P,R,S) \
 firstprivate(emlrtHadParallelError)

  {
    if (setjmp(b_emlrtJBEnviron) == 0) {
      st.prev = sp;
      st.tls = emlrtAllocTLS(sp, omp_get_thread_num());
      st.site = NULL;
      emlrtSetJmpBuf(&st, &b_emlrtJBEnviron);
    } else {
      emlrtHadParallelError = true;
    }

#pragma omp for nowait

    for (k = 0; k <= ub_loop; k++) {
      if (emlrtHadParallelError)
        continue;
      if (setjmp(b_emlrtJBEnviron) == 0) {
        if ((x_data[k] > 1.0) || (x_data[k] < -1.0) || muDoubleScalarIsNaN
            (x_data[k])) {
          y = rtNaN;
        } else if (x_data[k] == 1.0) {
          y = rtInf;
        } else if (x_data[k] == -1.0) {
          y = rtMinusInf;
        } else {
          if (x_data[k] < -0.7) {
            z = muDoubleScalarSqrt(-muDoubleScalarLog((x_data[k] + 1.0) / 2.0));
            y = -(((1.641345311 * z + 3.429567803) * z + -1.624906493) * z +
                  -1.970840454) / ((1.6370678 * z + 3.5438892) * z + 1.0);
          } else if (x_data[k] > 0.7) {
            z = muDoubleScalarSqrt(-muDoubleScalarLog((1.0 - x_data[k]) / 2.0));
            y = (((1.641345311 * z + 3.429567803) * z + -1.624906493) * z +
                 -1.970840454) / ((1.6370678 * z + 3.5438892) * z + 1.0);
          } else {
            z = x_data[k] * x_data[k];
            y = x_data[k] * (((-0.140543331 * z + 0.914624893) * z +
                              -1.645349621) * z + 0.886226899) / ((((0.012229801
              * z + -0.329097515) * z + 1.442710462) * z + -2.118377725) * z +
              1.0);
          }

          if (x_data[k] > 0.5) {
            z = -(eml_erfcore(y) - (1.0 - x_data[k])) / (1.1283791670955126 *
              muDoubleScalarExp(-y * y));
            y -= z / (y * z + 1.0);
            z = -(eml_erfcore(y) - (1.0 - x_data[k])) / (1.1283791670955126 *
              muDoubleScalarExp(-y * y));
            y -= z / (y * z + 1.0);
          } else if (x_data[k] < -0.5) {
            z = (eml_erfcore(-y) - (x_data[k] + 1.0)) / (1.1283791670955126 *
              muDoubleScalarExp(-y * y));
            y -= z / (y * z + 1.0);
            z = (eml_erfcore(-y) - (x_data[k] + 1.0)) / (1.1283791670955126 *
              muDoubleScalarExp(-y * y));
            y -= z / (y * z + 1.0);
          } else {
            /* ========================== COPYRIGHT NOTICE ============================ */
            /*  The algorithms for calculating ERF(X) and ERFC(X) are derived           */
            /*  from FDLIBM, which has the following notice:                            */
            /*                                                                          */
            /*  Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.       */
            /*                                                                          */
            /*  Developed at SunSoft, a Sun Microsystems, Inc. business.                */
            /*  Permission to use, copy, modify, and distribute this                    */
            /*  software is freely granted, provided that this notice                   */
            /*  is preserved.                                                           */
            /* =============================    END    ================================ */
            absx = muDoubleScalarAbs(y);
            if (muDoubleScalarIsNaN(y)) {
              z = y;
            } else if (muDoubleScalarIsInf(y)) {
              if (y < 0.0) {
                z = -1.0;
              } else {
                z = 1.0;
              }
            } else if (absx < 0.84375) {
              if (absx < 3.7252902984619141E-9) {
                if (absx < 2.8480945388892178E-306) {
                  z = 0.125 * (8.0 * y + 1.0270333367641007 * y);
                } else {
                  z = y + 0.12837916709551259 * y;
                }
              } else {
                z = y * y;
                z = y + y * ((z * (z * (z * (z * -2.3763016656650163E-5 +
                  -0.0057702702964894416) + -0.02848174957559851) +
                                   -0.3250421072470015) + 0.12837916709551256) /
                             (z * (z * (z * (z * (z * -3.9602282787753681E-6 +
                  0.00013249473800432164) + 0.0050813062818757656) +
                  0.0650222499887673) + 0.39791722395915535) + 1.0));
              }
            } else if (absx < 1.25) {
              P = (absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) *
                ((absx - 1.0) * ((absx - 1.0) * -0.0021663755948687908 +
                                 0.035478304325618236) + -0.11089469428239668) +
                0.31834661990116175) + -0.37220787603570132) +
                                  0.41485611868374833) + -0.0023621185607526594;
              z = (absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) *
                ((absx - 1.0) * ((absx - 1.0) * 0.011984499846799107 +
                                 0.013637083912029051) + 0.12617121980876164) +
                0.071828654414196266) + 0.540397917702171) + 0.10642088040084423)
                + 1.0;
              if (y >= 0.0) {
                z = P / z + 0.84506291151046753;
              } else {
                z = -0.84506291151046753 - P / z;
              }
            } else if (absx > 6.0) {
              if (y < 0.0) {
                z = -1.0;
              } else {
                z = 1.0;
              }
            } else {
              z = 1.0 / (absx * absx);
              if (absx < 2.8571434020996094) {
                R = z * (z * (z * (z * (z * (z * (z * -9.8143293441691455 +
                  -81.2874355063066) + -184.60509290671104) +
                            -162.39666946257347) + -62.375332450326006) +
                              -10.558626225323291) + -0.69385857270718176) +
                  -0.0098649440348471482;
                S = z * (z * (z * (z * (z * (z * (z * (z * -0.0604244152148581 +
                  6.5702497703192817) + 108.63500554177944) + 429.00814002756783)
                            + 645.38727173326788) + 434.56587747522923) +
                              137.65775414351904) + 19.651271667439257) + 1.0;
              } else {
                R = z * (z * (z * (z * (z * (z * -483.5191916086514 +
                  -1025.0951316110772) + -637.56644336838963) +
                                   -160.63638485582192) + -17.757954917754752) +
                         -0.799283237680523) + -0.0098649429247001;
                S = z * (z * (z * (z * (z * (z * (z * -22.440952446585818 +
                  474.52854120695537) + 2553.0504064331644) + 3199.8582195085955)
                                   + 1536.729586084437) + 325.79251299657392) +
                         30.338060743482458) + 1.0;
              }

              b_log2(absx, &P, &z);
              z = muDoubleScalarFloor(P * 2.097152E+6) / 2.097152E+6 *
                muDoubleScalarPower(2.0, z);
              z = muDoubleScalarExp(-z * z - 0.5625) * muDoubleScalarExp((z -
                absx) * (z + absx) + R / S) / absx;
              if (y < 0.0) {
                z--;
              } else {
                z = 1.0 - z;
              }
            }

            z = (z - x_data[k]) / (1.1283791670955126 * muDoubleScalarExp(-y * y));
            y -= z / (y * z + 1.0);

            /* ========================== COPYRIGHT NOTICE ============================ */
            /*  The algorithms for calculating ERF(X) and ERFC(X) are derived           */
            /*  from FDLIBM, which has the following notice:                            */
            /*                                                                          */
            /*  Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.       */
            /*                                                                          */
            /*  Developed at SunSoft, a Sun Microsystems, Inc. business.                */
            /*  Permission to use, copy, modify, and distribute this                    */
            /*  software is freely granted, provided that this notice                   */
            /*  is preserved.                                                           */
            /* =============================    END    ================================ */
            absx = muDoubleScalarAbs(y);
            if (muDoubleScalarIsNaN(y)) {
              z = y;
            } else if (muDoubleScalarIsInf(y)) {
              if (y < 0.0) {
                z = -1.0;
              } else {
                z = 1.0;
              }
            } else if (absx < 0.84375) {
              if (absx < 3.7252902984619141E-9) {
                if (absx < 2.8480945388892178E-306) {
                  z = 0.125 * (8.0 * y + 1.0270333367641007 * y);
                } else {
                  z = y + 0.12837916709551259 * y;
                }
              } else {
                z = y * y;
                z = y + y * ((z * (z * (z * (z * -2.3763016656650163E-5 +
                  -0.0057702702964894416) + -0.02848174957559851) +
                                   -0.3250421072470015) + 0.12837916709551256) /
                             (z * (z * (z * (z * (z * -3.9602282787753681E-6 +
                  0.00013249473800432164) + 0.0050813062818757656) +
                  0.0650222499887673) + 0.39791722395915535) + 1.0));
              }
            } else if (absx < 1.25) {
              P = (absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) *
                ((absx - 1.0) * ((absx - 1.0) * -0.0021663755948687908 +
                                 0.035478304325618236) + -0.11089469428239668) +
                0.31834661990116175) + -0.37220787603570132) +
                                  0.41485611868374833) + -0.0023621185607526594;
              z = (absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) * ((absx - 1.0) *
                ((absx - 1.0) * ((absx - 1.0) * 0.011984499846799107 +
                                 0.013637083912029051) + 0.12617121980876164) +
                0.071828654414196266) + 0.540397917702171) + 0.10642088040084423)
                + 1.0;
              if (y >= 0.0) {
                z = P / z + 0.84506291151046753;
              } else {
                z = -0.84506291151046753 - P / z;
              }
            } else if (absx > 6.0) {
              if (y < 0.0) {
                z = -1.0;
              } else {
                z = 1.0;
              }
            } else {
              z = 1.0 / (absx * absx);
              if (absx < 2.8571434020996094) {
                R = z * (z * (z * (z * (z * (z * (z * -9.8143293441691455 +
                  -81.2874355063066) + -184.60509290671104) +
                            -162.39666946257347) + -62.375332450326006) +
                              -10.558626225323291) + -0.69385857270718176) +
                  -0.0098649440348471482;
                S = z * (z * (z * (z * (z * (z * (z * (z * -0.0604244152148581 +
                  6.5702497703192817) + 108.63500554177944) + 429.00814002756783)
                            + 645.38727173326788) + 434.56587747522923) +
                              137.65775414351904) + 19.651271667439257) + 1.0;
              } else {
                R = z * (z * (z * (z * (z * (z * -483.5191916086514 +
                  -1025.0951316110772) + -637.56644336838963) +
                                   -160.63638485582192) + -17.757954917754752) +
                         -0.799283237680523) + -0.0098649429247001;
                S = z * (z * (z * (z * (z * (z * (z * -22.440952446585818 +
                  474.52854120695537) + 2553.0504064331644) + 3199.8582195085955)
                                   + 1536.729586084437) + 325.79251299657392) +
                         30.338060743482458) + 1.0;
              }

              b_log2(absx, &P, &z);
              z = muDoubleScalarFloor(P * 2.097152E+6) / 2.097152E+6 *
                muDoubleScalarPower(2.0, z);
              z = muDoubleScalarExp(-z * z - 0.5625) * muDoubleScalarExp((z -
                absx) * (z + absx) + R / S) / absx;
              if (y < 0.0) {
                z--;
              } else {
                z = 1.0 - z;
              }
            }

            z = (z - x_data[k]) / (1.1283791670955126 * muDoubleScalarExp(-y * y));
            y -= z / (y * z + 1.0);
          }
        }

        z1_data[k] = y;
      } else {
        emlrtHadParallelError = true;
      }
    }
  }

  emlrtPopJmpBuf(sp, &emlrtJBStack);
  emlrtExitParallelRegion(sp, omp_in_parallel());
}

/* End of code generation (applyScalarFunction.c) */
