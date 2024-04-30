<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    title-text="Professional Data"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="question_completed && can_advance"
    
  >
    <div
      class="mb-4"
    >
    {{ state_view }}
    <p>
      Edwin Hubble's own data from 1929 is shown in purple. (Your class's data is shown in blue).
    </p>

    <p>
      Does your class's age estimate agree with Hubble's age estimate? It might help to show <strong>fit lines to data</strong> (using <v-icon>mdi-chart-timeline-variant</v-icon>).
    </p>

    <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="[
            'Yes',
            'No',
            'I\'m not sure',
          ]"
          :feedbacks="[
            'Remember, the slope of the line is related to the age measurement from this data. Are the slopes the same?',
            'Correct. The best fit lines for our data and Edwin Hubble\'s data have very different slopes, so they have different ages.',
            'The slope of the line is related to the age measurement from this data. Are the slopes the same?']"
          :incorrect-answers="[0]"
          :correct-answers="[1]"
          :neutral-answers="[2]"
          @select="(status) => { if (status.correct) { question_completed = true;  log(status); } }"
          :score-tag="state_view.score_tag"
          @mc-initialize-response="mc_callback(['mc-initialize-response',$event])"
          @mc-score="mc_callback(['mc-score',$event])"
          :initialization="state_view.mc_score"
        >
        <!-- @mc-initialize-response="mc_initialize_response_callback($event)"
          @mc-score="mc_score_callback($event)" -->
        </mc-radiogroup>
      </v-container>
    </div>
  </scaffold-alert>
</template>

<script>
module.exports = {
  data() {
    return {
      question_completed: false,
    };
  },
  
  methods: {
    log(val) {
      console.log(val);
    },
  }
};
</script>
