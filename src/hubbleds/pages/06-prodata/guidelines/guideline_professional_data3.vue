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
        Whose data set has more random uncertainty?
      </p>
      
      <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="[
            'Our class\'s dataset',
            'Edwin Hubble\'s dataset',
            'It\'s hard to tell',
          ]"
          :feedbacks='[
            "Yes. We can see how much more our data deviates from the best fit line.",
            "It can be hard to tell. One thing to consider is how far off your data is from the best fit line",
            "It can be hard to tell. One thing to consider is how far off your data is from the best fit line",
          ]'
          :correct-answers="[0]"
          :neutral-answers='[1,2]'
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
