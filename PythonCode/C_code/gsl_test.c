#include <stdio.h>
#include <gsl/gsl_blas.h>

int
main (void)
{

  double *a = malloc(sizeof(double[4]));
  double *b = malloc(sizeof(double[4]));
  double *c = malloc(sizeof(double[4]));

  int i;
  for(int i=0; i<4; i++){
      a[i] = 0.5;
      b[i] = 2;
      c[i] = 0;
  }

  gsl_matrix_view A = gsl_matrix_view_array(a, 2, 2);
  gsl_matrix_view B = gsl_matrix_view_array(b, 2, 2);
  gsl_matrix_view C = gsl_matrix_view_array(c, 2, 2);

  /* Compute C = A B */

  gsl_blas_dgemm (CblasNoTrans, CblasNoTrans,
                  1.0, &A.matrix, &B.matrix,
                  0.0, &C.matrix);

  printf ("[ %g, %g\n", c[0], c[1]);
  printf ("  %g, %g ]\n", c[2], c[3]);

  return 0;
}