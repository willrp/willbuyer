//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { Image, Grid, Card } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ResponsiveGrid from "components/util/responsive-grid";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

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
        padding: "0.5em",
        display: "flex",
        justifyContent: "center"
    }
})

const cardClass = css({
    "&&&&&": {
        flexGrow: 1,
        margin: 0
    },
    "&&&&& .header": {
        fontSize: "1.1em"
    },
    "&&&&& .meta": {
        textDecoration: "line-through"
    },
    "&&&&& .description": {
        margin: 0,
        color: "red"
    }
})

//COMPONENT=================================================================
function ProductGrid({ products }) {
    function renderProducts() {
        return products.map(
            (item) => {
                const { image, name, price, discount, id } = item;
                return (
                    <Grid.Column key={id} className={columnClass}>
                        <Card className={cardClass} as={Link} to={`/product/${id}`}>
                            <Image src={image} wrapped ui={false} />
                            <Card.Content>
                                <Card.Header textAlign="center">{name}</Card.Header>
                                <Card.Meta textAlign="center">{price.symbol}{price.retail.toFixed(2)}</Card.Meta>
                                <Card.Description as="h4" textAlign="center">
                                    {price.symbol}{price.outlet.toFixed(2)} ({discount.toFixed(0) + "% OFF"})
                                </Card.Description>
                            </Card.Content>
                        </Card>
                    </Grid.Column>
                )
            }
        )
    }

    function render() {
        return (
            <ResponsiveGrid
                className={gridClass}
                largescreen={5}
                computer={4}
                tablet={3}
                mobile={2}
            >
                {renderProducts()}
            </ResponsiveGrid>
        )
    }
    
    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductGrid;