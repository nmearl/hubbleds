<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto angsize_alert"
    max-width="800"
    elevation="6"
    header-text="Estimate Distance"
    @back="state.marker_backward = 1"
    @next="() => {
      state.marker_forward = 1;
      state.distance_calc_count += 1;
      state.show_ruler = false;
    }"
  >
    <div
      class="mb-4"
      v-intersect="checkIntersecting"
    >
      <p class="mb-4">
        You entered:
      </p>
      <v-card
        class="JaxEquation pa-3"
        color="info lighten-1"
        elevation="0"
      >
        $$ D = \frac{ {{ Math.round(state.distance_const) }} }{\textcolor{black}{\colorbox{#FFAB91}{ {{ (state.meas_theta).toFixed(0) }} } } } \text{ Mpc}$$
      </v-card>    
      <p class="mt-4">
        Dividing through gives you the estimated distance to your galaxy:
      </p>
      <div
        class="JaxEquation my-8"
      >
        $$ D = {{ (Math.round(state.distance_const)/state.meas_theta).toFixed(0) }} \text{ Mpc} $$
      </div>
      <v-divider role="presentation" class="mt-3"></v-divider>
      <v-card
        outlined
        class="legend mt-8"
        color="info"
      >
        <v-container>
          <v-row
            no-gutters
          >
            <v-col>
              <div
                class="JaxEquation"
              >
                $$ D = \frac{ {{ Math.round(state.distance_const) }} }{\theta \text{ (in arcsec)} } \text{ Mpc}$$
              </div>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col>
              \(D\)
            </v-col>
            <v-col
              cols="10"
            >
              distance to your galaxy, in Mpc
            </v-col>
          </v-row>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col
              cols="2"
            >
              \(&theta;\)
            </v-col>
            <v-col
              cols="10"
            >
              angular size of your galaxy, in arcseconds
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </div>
  </scaffold-alert> 
</template>

<script>
module.exports = {
 props: ['state'],
  computed: {
   checkIntersecting(entries, _observer, intersecting) { if (intersecting) { window.MathJax.typesetPromise(entries.map(entry => entry.target)) }}
  }
}
</script>

<style>

.JaxEquation .MathJax {
  margin: 16px auto !important;
}

mjx-mfrac {
  margin: 0 4px !important;
}

mjx-mstyle {
  border-radius: 5px;
}

.angsize_alert .v-alert {
  font-size: 16px !important;
}

.v-application .legend {
  border: 1px solid white !important;
  max-width: 300px;
  margin: 0 auto 0;
  font-size: 15px !important;
}

#gal_ang_size {
  color:  black;
  font-size: 18px;
  font-family: "Roboto", Arial, Helvetica, sans-serif;
  padding: 3px;
}

</style>

