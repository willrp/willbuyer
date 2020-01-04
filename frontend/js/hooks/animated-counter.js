//IMPORT EXTERNAL COMPONENTS================================================
import { useState, useEffect } from "react";

//COMPONENT=================================================================
function useAnimatedCounter(value, integer=true) {
    const [counter, setCounter] = useState(0);

    useEffect(() => {
        let current = counter;
        const interval = setInterval(function(){
            if(current === value) {
                clearInterval(interval);
            }
            else{
                if(integer) {
                    const step = (value - current) * 0.02;
                    const normstep = (value > current) ? Math.ceil(step) : Math.floor(step);
                    current = current + normstep;
                    setCounter(current);
                }
                else{
                    const intvalue = Math.round(value * 100);
                    const intcurrent = Math.round(current * 100);
                    const step = (intvalue - intcurrent) * 0.15;
                    const normstep = (intvalue > intcurrent) ? Math.ceil(step) : Math.floor(step);
                    current = (intcurrent + normstep) / 100;
                    setCounter(current);
                }
            }
        }, 5);
    }, [value])

    return counter;
}

//EXPORT COMPONENT==========================================================
export default useAnimatedCounter;