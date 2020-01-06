//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useEffect } from "react";
import { useRouteMatch } from "react-router";
import { useHistory } from "react-router-dom";
import Slider, {createSliderWithTooltip} from 'rc-slider';

const Range = createSliderWithTooltip(Slider.Range);

//IMPORT EXTERNAL FUNCTIONS=================================================
import queryString from "query-string";
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const rangeClass = css({
    "&&&&&": {
        marginBottom: "1em"
    },
    "&&&&& .rc-slider-track": {
        background: "deepskyblue"
    }
})

//COMPONENT=================================================================
function PriceRange({ pricerange, pickedrange, executeOnChange }) {
    let history = useHistory();
    const match = useRouteMatch();
    const valuerange = (pickedrange === null) ? pricerange : pickedrange;
    const [currentValue, setCurrentValue] = useState([valuerange.min, valuerange.max])

    useEffect(() => {
        setCurrentValue([valuerange.min, valuerange.max])
    }, valuerange)

    function changeValue(value) {
        if (value[0] !== value[1]){
            setCurrentValue(value);
        }
    }

    function changePickedRange(value) {
        const range = {
            min: value[0],
            max: value[1]
        }
        executeOnChange();
        history.push(`${match.url}?${queryString.stringify(range, {sort: false})}`);
    }

    function render() {
        const symbol = "£";
        const marks = JSON.parse('{"' + pricerange.min + '": "' + symbol + pricerange.min + '","' + (pricerange.max) + '": "'+ symbol + (pricerange.max) + '"}');
        const diff = (pricerange.max - pricerange.min);
        const step = (diff > 0) ? 1 : null;
        return (
            <Range
                className={rangeClass}
                tipFormatter={(value) => symbol + value}
                min={pricerange.min}
                max={pricerange.max}
                marks={marks}
                value={currentValue}
                defaultValue={currentValue}
                step={step}
                count={1}
                allowCross={false}
                onChange={changeValue}
                onAfterChange={changePickedRange}
            />
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default PriceRange;