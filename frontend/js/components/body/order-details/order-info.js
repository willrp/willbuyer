//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Grid, Header, Statistic, Segment } from "semantic-ui-react";

//IMPORT HOOKS==============================================================
import useAnimatedCounter from "hooks/animated-counter";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";
import moment from "moment";

//STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&&": {
        margin: "0",
        marginBottom: "1em"
    },
    "&&&&&>.row": {
        padding: "0"
    },
    "&&&&& .column": {
        padding: "0"
    },
    "&&&&& .segment": {
        padding: "0.25em",
        width: "100%",
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
})

const priceClass = css({
    "&&&&& .titleClass": {
        fontWeight: "bold",
        marginBottom: "0.25em"
    },
    "&&&&& .priceMetaClass": {
        textDecoration: "line-through",
        opacity: 0.4,
        marginBottom: "0.5em"
    },
    "&&&&& .priceHeaderClass": {
        color: "red",
        marginTop: "0"
    }
})

const discountClass = css({
    "&&&&& .statistic>div": {
        color: "red"
    }
})

//COMPONENT=================================================================
function OrderInfo({ product_types, items_amount, total, updated_at }) {
    const productvalue = useAnimatedCounter(product_types);
    const itemsvalue = useAnimatedCounter(items_amount);

    const { symbol, retail, outlet } = total;
    const retailvalue = useAnimatedCounter(retail, false);
    const outletvalue = useAnimatedCounter(outlet, false);

    const discount = Math.floor((1.0 - (outlet / retail)) * 100);
    const discountvalue = useAnimatedCounter(discount);

    const updatedAtMoment = moment(updated_at);

    function render() {
        return (
            <Grid
                className={gridClass}
                columns="equal"
            >
                <Grid.Row>
                    <Grid.Column>
                        <Segment textAlign="center">
                            <Statistic size="mini" horizontal>
                                <Statistic.Label>Order Placed:</Statistic.Label>
                                <Statistic.Value>{updatedAtMoment.format("YYYY-MM-DD ddd")}</Statistic.Value>
                            </Statistic>
                        </Segment>
                    </Grid.Column>
                    <Grid.Column>
                        <Segment textAlign="center">
                            <Statistic size="mini" horizontal>
                                <Statistic.Label>Time:</Statistic.Label>
                                <Statistic.Value>{updatedAtMoment.format("HH:mm:ss")} JST</Statistic.Value>
                            </Statistic>
                        </Segment>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column>
                        <Segment textAlign="center">
                            <Statistic>
                                <Statistic.Value>{productvalue}</Statistic.Value>
                                <Statistic.Label>Products</Statistic.Label>
                            </Statistic>
                        </Segment>
                    </Grid.Column>
                    <Grid.Column>
                        <Segment textAlign="center">
                            <Statistic>
                                <Statistic.Value>{itemsvalue}</Statistic.Value>
                                <Statistic.Label>Items</Statistic.Label>
                            </Statistic>
                        </Segment>
                    </Grid.Column>
                    <Grid.Column>
                        <Segment textAlign="center" className={priceClass}>
                            <div>
                                <p className="titleClass">Total Price:</p>
                                <p className="priceMetaClass">{symbol}{retailvalue.toFixed(2)}</p>
                                <Header as="h2" className="priceHeaderClass">{symbol}{outletvalue.toFixed(2)}</Header>
                            </div>
                        </Segment>
                    </Grid.Column>
                    <Grid.Column>
                        <Segment textAlign="center" className={discountClass}>
                            <Statistic>
                                <Statistic.Value>{discountvalue}%</Statistic.Value>
                                <Statistic.Label>Off</Statistic.Label>
                            </Statistic>
                        </Segment>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default OrderInfo;