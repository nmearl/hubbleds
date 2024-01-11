<template>
  <scaffold-alert
    header-text="Estimate Distance"
    @back="
      state.marker = 'est_dis1';
    "
    @next="() => { 
      state.marker = 'cho_row2';
      state.galaxy_selected = false;
    }"
  >
    <div
      class="mb-4"
      v-intersect="checkIntersecting"
    >
      <p>
        Recall, if we assume a galaxy is the <strong>same size as our Milky Way galaxy</strong>, the distance to the galaxy can be found using:
      </p>
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
                $$ D = \frac{ {{ Math.round(state.distance_const) }} }{\theta \text{ (in arcsec)}} \text{ Mpc} $$
              </div>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col
              
            >
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
      <p>

      </p>
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

.JaxEquation {
  margin: 0;
}

.JaxEquation .MathJax {
  margin: 0 auto 16px !important;
}

.v-application .legend {
  border: 1px solid white !important;
  max-width: 300px;
  margin: 0 auto 0;
  font-size: 15px !important;
}

</style>
