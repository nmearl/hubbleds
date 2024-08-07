<template>
  <scaffold-alert
    header-text="Class Age Range"
    next-text="check"
    @back="back_callback()"
    @next="() => {
      const expectedAnswers = [state_view.student_low_age, state_view.student_high_age];
      if (validateAnswersJS(['low_age', 'high_age'], expectedAnswers)) {
        next_callback();
      }
    }"
    :can-advance="can_advance"
  >
    <div
      class="mb-4"
      v-intersect="typesetMathJax"
    >
      <p>
        Let's consider the range of age estimates for the universe obtained by you and your classmates.
      </p>
      <p>
        Enter the lowest and highest age estimates from your class here:
      </p>
      <div
        class="JaxEquation my-8"
      >
        $$ \text{Lowest age:  } \bbox[#FBE9E7]{\input[low_age][]{} } \text{ Gyr} $$
        $$ \text{Highest age:  } \bbox[#FBE9E7]{\input[high_age][]{} } \text{ Gyr} $$
      </div>
    </div>
    <v-divider
      class="my-4"
      v-if="failedValidationAgeRange"
    >
    </v-divider>
    <v-alert
      v-if="failedValidationAgeRange"
      dense
      color="info darken-1"
    >
      Not quite. Make sure you are entering the highest and lowest values for the entire class. Enter only whole integers.
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
export default {

  data: function() {
    return {
      failedValidationAgeRange: false
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
        this.failedValidationAgeRange = (value != null && value === expectedAnswers[index]) ? false : true;
        console.log("expectedAnswer", expectedAnswers);
        console.log("entered value", value);
        return value != null && value === expectedAnswers[index];
      });
    },

    typesetMathJax(entries, _observer, intersecting) {
      if (intersecting) {
        MathJax.typesetPromise(entries.map(entry => entry.target));
      }
    },
  }
};
</script>
