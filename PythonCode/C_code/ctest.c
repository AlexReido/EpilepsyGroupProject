#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <complex.h>  
#include <gsl/gsl_sf_bessel.h>  /* Standard Library of Complex Numbers */
#include <gsl/gsl_blas.h>

// A is m rows by k columns
// B is k rows by n columns
// C is m rows by n columns
void multiply(double *A, int row1, int col1, double *B, int row2, int col2, double *C) {
    for (int i = 0; i < row1; i++) {
        for (int j = 0; j < col2; j++) {
            int sum = 0;
            for (int k = 0; k < col1; k++){
                sum = sum + A[i * col1 + k] * B[k * col2 + j];
            }
            C[i * col2 + j] = sum;
        }
    }
}

void cfun(const int t, double *wnet, const int nodes, double *x, double *rand_i_sig) {
    const double dist = -1.2;
    size_t i,j, time;

    double (*theta)[nodes] = malloc(sizeof(double[t][nodes]));

    double initial_theta = -1 * acos((1 + dist) / (1 - dist));  // creal removed?
    for (j=0; j < nodes; j++){
        theta[0][j] = initial_theta;  // probably blas to do this
    }

    double *cos_theta_old = malloc(sizeof(double[nodes]));
    double *theta_diff = malloc(sizeof(double[nodes]));
    double *ictogenicity = malloc(sizeof(double[nodes]));
    double *dot = malloc(sizeof(double[nodes]));

    gsl_matrix_view A;
    gsl_matrix_view B;
    gsl_matrix_view C;

    for (time = 1; time < t; time++){
        for(i=0; i<nodes; i++){
            cos_theta_old[i] = cos(theta[time-1][i]);  // find all
        }

        // find array of theta differences
        for(i=0; i<nodes; i++){
            theta_diff[i] = 1 - cos(theta[time-1][i] - initial_theta);
        }
        A = gsl_matrix_view_array(wnet, nodes, nodes);
        B = gsl_matrix_view_array(theta_diff, nodes, 1);
        C = gsl_matrix_view_array(dot, nodes, 1);
        gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, &A.matrix, &B.matrix, 0.0, &C.matrix);
        for(i=0; i<nodes; i++){
            ictogenicity[i] = dist + rand_i_sig[(time*nodes)+i] + dot[i];  // TODO use random_normal() here instead
        }

        for(j=0; j<nodes; j++){
            theta[time][j] = theta[time-1][j] + (0.01 * (1 - cos_theta_old[j] + ((1 + cos_theta_old[j]) * ictogenicity[j])));
        }
    }
    for (int i=0; i<t; i++){
        for (int j=0; j<nodes; j++){
            x[i * nodes + j] = (1 - cos(theta[i][j] - initial_theta) * 0.5) > 0.9;
        }
    }
    // need 20489 ones
}

int main(){
    const int t = 4000000;
    const int nodes = 59;
    double *wnet = malloc(sizeof(double[nodes*nodes]));
    double *x = malloc(sizeof(double[nodes*t]));;
    double *rand_i_sig = malloc(sizeof(double[nodes*t]));;

    int i,j;
    for(int i=0; i<nodes; i++){
        for(int j=0; j<nodes; j++){
            wnet[(i * nodes) + j] = 0.5;
        }
    }

    for(int i=0; i<t; i++){
        for(int j=0; j<nodes; j++){
            x[i * nodes + j] = 0;
        }
    }

    for(int i=0; i<nodes; i++){
        for(int j=0; j<t; j++){
            rand_i_sig[i * nodes + j] = 1;
        }
    }

    cfun(t, wnet, nodes, x, rand_i_sig);

    return 0;
}
