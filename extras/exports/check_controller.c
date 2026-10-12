/* Exercise the exported C API. The controller equations remain in Modelica. */
#include "HoverController.h"
#include <stdio.h>

int main(void) {
    HoverControllerState state;
    HoverController_startup(&state);
    HoverController_recalibrate(&state);
    float z_ref, z, vz;
    while (scanf("%f %f %f", &z_ref, &z, &vz) == 3) {
        state.z_ref = z_ref;
        state.z = z;
        state.vz = vz;
        HoverController_dostep(&state);
        if (state.rumoca_galec_error_signal_status != 0U) return 1;
        printf("%.9g\n", (double)state.T);
    }
    return ferror(stdin) ? 2 : 0;
}
