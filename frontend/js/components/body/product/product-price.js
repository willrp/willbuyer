//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Header, Segment, Statistic } from "semantic-ui-react";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const priceClass = css({
    "&&&&&>.segment": {
        width: "50%"
    },
    "&&&&& .priceMetaClass": {
        textDecoration: "line-through",
        opacity: 0.4,
        marginBottom: "0.5em"
    },
    "&&&&& .priceHeaderClass": {
        color: "red",
        marginTop: "0"
    },
    "&&&&& .statistic>div": {
        color: "red"
    }
})

const discountClass = css({
    "&&&&&": {
        backgroundColor: "#D70000"
    },
    "&&&&& .statistic>div": {
        color: "white"
    }
})

//COMPONENT=================================================================
function ProductPrice({ symbol, retail, outlet }) {
    function render() {
        const discount = Math.floor((1.0 - (outlet / retail)) * 100);
        return (
            <Segment.Group horizontal className={priceClass}>
                <Segment textAlign="center">
                    <p className="priceMetaClass">{symbol}{retail.toFixed(2)}</p>
                    <Header as="h1" className="priceHeaderClass">{symbol}{outlet.toFixed(2)}</Header>
                </Segment>
                <Segment textAlign="center" className={discountClass}>
                    <Statistic>
                        <Statistic.Value>{discount}%</Statistic.Value>
                        <Statistic.Label>Off</Statistic.Label>
                    </Statistic>
                </Segment>
            </Segment.Group>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductPrice;