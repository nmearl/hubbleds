<!-- # multiple choice -->
<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="question_completed && can_advance"
    
  >
    <div
      class="mb-4"
    >
      <p>
        Why do you think scientists' measurements of the age of the universe have changed with time?
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="[
              'Scientists do not really know how to measure the age of the universe.',
              'Scientists measure different ages because the universe is always getting older.',
              'The measured age of the universe can change based on new and better data.'
          ]"
          :feedbacks="[
            'It is possible to measure the age of the universe, though it can be difficult to do so.',
            'The universe is always getting older, but scientists measure the age of the universe on scales of billions of years, far greater than time between recent measurements.',
            'Correct! Improved data and technology allow scientists to measure the age of the universe more precisely and with less bias.'
          ]"
          :correct-answers="[2]"
          :neutral-answers='[0,1]'
          @select="(status) => { if (status.correct) { question_completed = true; } }"
          :score-tag="state_view.score_tag"
          @mc-initialize-response="mc_callback(['mc-initialize-response',$event])"
          @mc-score="mc_callback(['mc-score',$event])"
          :initialization="state_view.mc_score"
        >
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
};
</script>
