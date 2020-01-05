//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { Grid, Segment, Statistic, Button } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ResponsiveGrid from "components/util/responsive-grid";

//IMPORT HOOKS==============================================================
import useIsPhone from "hooks/is-phone";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";
import moment from "moment";

//STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&&": {
        margin: "0",
        marginTop: "1em",
        marginBottom: "0.5em"
    }
})

const columnClass = css({
    "&&&&&": {
        padding: "0.25em",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    }
})

const segmentGroupClass = css({
    "&&&&&": {
        margin: "0",
        flexGrow: 1
    },
    "&&&&&>.segments": {
        margin: "0",
        border: "0",
        flexGrow: 1
    },
    "&&&&& .segment": {
        padding: "0.5em",
        border: "0"
    },
    "&&&&&>.segments:last-child>.segment:last-child": {
        padding: "0",
        minHeight: "50%",
        display: "flex",
        flexGrow: 1,
        alignItems: "stretch"
    },
    "&&&&& .button": {
        margin: "0",
        color: "black",
        backgroundColor: "lightskyblue",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    "&&&&& .button:hover": {
        color: "white",
        backgroundColor: "deepskyblue"
    },
})

//COMPONENT=================================================================
function OrdersGrid({ orders }) {
    const isPhone = useIsPhone();

    function renderOrders() {
        return orders.map(
            (item) => {
                const { slug, product_types, items_amount, total, updated_at } = item;
                const { symbol, outlet } = total;
                const updatedAtMoment = moment(updated_at)
                return (
                    <Grid.Column key={slug} className={columnClass}>
                        <Segment.Group horizontal className={segmentGroupClass}>
                            <Segment.Group>
                                <Segment textAlign="center">
                                    <Statistic size="mini">
                                        <Statistic.Label>Order Placed</Statistic.Label>
                                        <Statistic.Value>{(isPhone) ? updatedAtMoment.format("YYYY-MM-DD") : updatedAtMoment.format("YYYY-MM-DD ddd")}</Statistic.Value>
                                    </Statistic>
                                </Segment>
                                <Segment textAlign="center">
                                    <Statistic size="mini">
                                        <Statistic.Label>Time</Statistic.Label>
                                        <Statistic.Value>{updatedAtMoment.format("HH:mm:ss")} JST</Statistic.Value>
                                    </Statistic>
                                </Segment>
                            </Segment.Group>
                            <Segment.Group>
                                <Segment textAlign="center">
                                    <Statistic size="mini">
                                        <Statistic.Label>Products</Statistic.Label>
                                        <Statistic.Value>{product_types}</Statistic.Value>
                                    </Statistic>    
                                </Segment>
                                <Segment textAlign="center">
                                    <Statistic size="mini">
                                        <Statistic.Label>Items</Statistic.Label>
                                        <Statistic.Value>{items_amount}</Statistic.Value>
                                    </Statistic>    
                                </Segment>
                            </Segment.Group>
                            <Segment.Group>
                                <Segment textAlign="center">
                                    <Statistic size="mini">
                                        <Statistic.Label>Total</Statistic.Label>
                                        <Statistic.Value>{symbol}{outlet.toFixed(2)}</Statistic.Value>
                                    </Statistic>    
                                </Segment>
                                <Segment>
                                    <Button 
                                        fluid
                                        as={Link}
                                        to={`/order/${slug}`}
                                    >
                                        Details
                                    </Button>
                                </Segment>
                            </Segment.Group>
                        </Segment.Group>
                    </Grid.Column>
                )
            }
        )
    }

    function render() {
        return (
            <ResponsiveGrid
                className={gridClass}
                largescreen={2}
                computer={2}
                tablet={1}
                mobile={1}
            >
                {renderOrders()}
            </ResponsiveGrid>
        )
    }
    
    return render()
}

//EXPORT COMPONENT==========================================================
export default OrdersGrid;