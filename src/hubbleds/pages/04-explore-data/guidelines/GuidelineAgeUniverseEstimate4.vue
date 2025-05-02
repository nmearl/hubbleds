<template>
  <scaffold-alert
    title-text="Estimate Age of Universe"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >
    <div
      class="mb-4"
      v-intersect="typesetMathJax"
    >
      <p class="mb-4">
        You entered:
      </p>
      <v-card
        class="JaxEquation pa-3 entered-card"
        color="info lighten-1"
        elevation="0"
      >
        $$ t =  {{ Math.round(state_view.age_const) }}   \times \frac{\textcolor{black}{\colorbox{#FFAB91}{ {{state_view.hypgal_distance.toFixed(0)}} } } \text{ Mpc} } { \textcolor{black}{\colorbox{#FFAB91}{ {{state_view.hypgal_velocity.toFixed(0)}} } }  \text{ km/s} }  \text{   Gyr}$$
      </v-card>    
      <p class="mt-4">
        Dividing through gives an estimated age of the universe from your dataset:
      </p>
      <div
        class="JaxEquation my-8 est-age"
      >

      $$ t = {{Math.round(this.state_view.age_const * state_view.hypgal_distance / state_view.hypgal_velocity).toFixed(0)}} \text{ Gyr} $$

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
                $$ t \text{ (in Gyr)}= {{ Math.round(state_view.age_const) }}  \times \frac{d \text{ (in Mpc)}}{v \text{ (in km/s)}} $$
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
              \(t\)
            </v-col>
            <v-col
              cols="10"
            >
              age of the universe, in Gyr. (1 Gyr = 1 billion years)
            </v-col>
          </v-row>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col
              cols="2"
            >
              \(d\)
            </v-col>
            <v-col
              cols="10"
            >
              distance the galaxy has traveled (distance to the galaxy, in Mpc)
            </v-col>
          </v-row>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col
              cols="2"
            >
              \(v\)
            </v-col>
            <v-col
              cols="10"
            >
              velocity of the galaxy (in km/s)
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </div>
  </scaffold-alert> 
</template>

<script>
module.exports = {

  methods: {
    typesetMathJax(entries, _observer, intersecting) {
      if (intersecting) {
        MathJax.typesetPromise(entries.map(entry => entry.target));
      }
    },
  },
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