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
      Is your age estimate higher or lower than the HST team's estimate?
      <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="[
            'Our class got a higher age estimate than HST',
            'Our class got a lower age estimate than HST',
            'The lines are too close to tell'
          ]"
          :feedbacks="feedbacks(state_view.hst_age, state_view.class_age)"
          :correct-answers="correctAnswers()"
          :neutral-answers="neutralAnswers()"
          @select="(status) => { if (status.correct) { question_completed = true; } }"
          :score-tag="state_view.score_tag"
          @mc-initialize-response="mc_callback(['mc-initialize-response',$event])"
          @mc-score="mc_callback(['mc-score',$event])"
          :initialization="state_view.mc_score"
        >
        </mc-radiogroup>
      <!-- <v-card color="secondary">
        <v-card-text>
          It's possible this card is giving incorrect feedback. Talk to a neighbor or instructor if you are unsure.
        </v-card-text>
      </v-card> -->
      </v-container>
    </div>
  </scaffold-alert>
</template>

<script setup>
module.exports = {
  props: ['state'],
  
  data() {
    return {
      question_completed: false,
    };
  },

  methods: {

    hst_age_less_then_class_age() {
      return parseFloat(this.state_viewhst_age) < parseFloat(this.state_viewclass_age)
    },

    too_close() {
      if (this.state_viewallow_too_close_correct) {
        return Math.abs(parseFloat(this.state_viewhst_age) - parseFloat(this.state_viewclass_age)) < this.state_viewages_within
      } else {
        // never too close with the zoom tool
        return false
      }
      
    },

    too_close_feedback() {

      if (!this.state_viewallow_too_close_correct) {
        // feedback for it's too close but we don't want to give away the correct answer
        return "Try again! Use the zoom tool to zoom in on the lines."
      }
      
      if (!this.too_close()) {
        // feedback for it's not too close, just...look harder
        return "Try again! You should be able to tell if your line has a shallower or steeper slope than the HST line."
      }
      
      if (this.hst_age_less_then_class_age()) {
        // feedback for too close but out class age is less than HST age (so class line is shallower)
        return "Correct! It is not always clear on visual inspection. However if you zoom in, you will notice that our class's line is slightly shallower than the HST line."
      } else {
        // feedback for too close but out class age is higher than HST age (so class line is steeper)
        return "Correct! It is not always clear on visual inspection. However if you zoom in, you will notice that class's line is slightly steeper than the HST line."
      }
      
    },
    
    feedbacks(hst_age, class_age) {
      // a shallower slope means a higher age
      // so if our slope is shallower than the HST slope, then our age is higher than the HST age
      if (this.hst_age_less_then_class_age()) {
        console.log('our slope is shallower than the HST slope')
        return ['Correct! The slope of best fit for our data is shallower than it is for the HST data',
          'Try again! Compare the slope of best fit for our data to the slope for the HST data',
          this.too_close_feedback()]
      } else {
        console.log('our slope is steeper than the HST slope')
        return ['Try again! Compare the slope of best fit for our data to the slope for the HST data',
          'Correct! The slope of best fit for our data is steeper than it is for the HST data',
          this.too_close_feedback()]
      }
      
    },

    correctAnswers() {
      if (this.hst_age_less_then_class_age()) {
        return this.too_close() ? [0,2] : [0]
      } else {
        return this.too_close() [1] ? [1,2] : [1]
      }
    },

    neutralAnswers() {
      if (this.hst_age_less_then_class_age()) {
        // return [1]
        return this.too_close() ? [1] : [1,2]
      } else {
        // return [0]
        return this.too_close() [0] ? [0] : [0,2]
      }
    }
  },

  
}
</script>
