<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto angsize_alert"
    max-width="800"
    elevation="6"
    title-text="Estimate Age of Universe"
    next-text="calculate"
    @back="state.marker = 'age_uni2'"
    @next="() => {
      const expectedAnswers = [state.hypgal_distance, state.hypgal_velocity];
      state.marker = validateAnswersJS(['gal_distance', 'gal_velocity'], expectedAnswers) ? 'age_uni4' : 'age_uni3';
    }"
  >

    <div
      class="mb-4"
      v-intersect="checkIntersecting"
    >
      <p>
        Enter the <strong>distance</strong> (in <strong>Mpc</strong>) and <strong>velocity</strong> (in <strong>km/s</strong>) of your hypothetical "Best Fit Galaxy" in the boxes.
      </p>
      <div
        class="JaxEquation my-8"
      >
        $$ t = {{ Math.round(state.age_const) }}  \times \frac{\bbox[#FBE9E7]{\input[gal_distance][]{} } \text{ Mpc} } { \bbox[#FBE9E7]{\input[gal_velocity][]{} } \text{ km/s} } \text{     Gyr}$$
      </div>
      <v-divider role="presentation"></v-divider>
      <div
        class="font-weight-medium mt-3"
      >
        Click <strong>CALCULATE</strong> to divide and estimate the age of the universe from your galaxy data set.
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
                $$ t \text{ (in Gyr)}= {{ Math.round(state.age_const) }}  \times \frac{d \text{ (in Mpc)}}{v \text{ (in km/s)}} $$
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
    <v-divider
      class="my-4"
      v-if="failedValidation"
    >
    </v-divider>
    <v-alert
      v-if="failedValidation"
      dense
      color="info darken-1"
    >
      Not quite. Make sure you are entering the values for the "Best Fit Galaxy" (in the bottom row of your table), with distance in the top box and velocity in the bottom box.
    </v-alert>
  </scaffold-alert> 
</template>

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


<script>
module.exports = {
  
  props: ['state'],

  data: function() {
    return {
      failedValidation: false
    }
  },

  methods: {
    getValue(inputID) {
      const input = document.getElementById(inputID);
      if (!input) { return null; }
      return input.value;
    },

    parseAnswer(inputID) {
      return parseFloat(this.getValue(inputID).replace(/,/g,''));
    },

    validateAnswersJS(inputIDs, expectedAnswers) {
      return inputIDs.every((id, index) => {
        const value = this.parseAnswer(id);
        this.failedValidation = (value && value === expectedAnswers[index]) ? false : true;
        console.log("expectedAnswer", expectedAnswers);
        console.log("entered value", value);
        return value && value === expectedAnswers[index];
      });
    }
  },
  computed: {
    checkIntersecting(entries, _observer, intersecting) { if (intersecting) { window.MathJax.typesetPromise(entries.map(entry => entry.target)) }}
  }
};
</script>

