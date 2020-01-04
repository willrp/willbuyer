//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Statistic } from "semantic-ui-react";

//IMPORT HOOKS==============================================================
import useAnimatedCounter from "hooks/animated-counter";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const statisticClass = css({
    "&&&&&": {
        margin: "0"
    }
})

//COMPONENT=================================================================
function Counter({ total }) {
    const counter = useAnimatedCounter(total);

    function render() {
        return (
            <Statistic className={statisticClass}>
                <Statistic.Value>{counter}</Statistic.Value>
                <Statistic.Label>{(counter === 1) ? "Product" : "Products"}</Statistic.Label>
            </Statistic>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Counter;