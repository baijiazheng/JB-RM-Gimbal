#include<stdio.h>
#include<stdint.h>

typedef struct{
    float last_out;
    uint8_t is_init;
}EmaState;

float ema_update(EmaState *state,float sample,float alpha){
    if (!state->is_init){
        state->last_out = sample;
        state->is_init = 1;
    }
    else{
        state->last_out = alpha * sample + (1.0f - alpha) * state->last_out;
    }
    return state->last_out;
}

void ema_reset(EmaState *state){
    state->is_init = 0;
    state->last_out = 0.0f;
}

int main (void){
    return 0;
}