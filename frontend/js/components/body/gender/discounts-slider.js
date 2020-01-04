//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { Image, Card, Segment } from "semantic-ui-react";
import Slider from "react-slick";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const slickClass = css({
    "&&&&&": {
        marginBottom: "3em"
    },
    "&&&&& .slick-track": {
        display: "flex"
    },
    "&&&&& .slick-slide": {
        height: "inherit",
        paddingRight: "1px"
    },
    "&&&&& .slick-slide>div, &&&&& .segment, &&&&& .card": {
        height: "100%"
    },
    "&&&&& .segment": {
        padding: "0.5em"
    },
    "&&&&& .card .header": {
        fontSize: "1em"
    },
    "&&&&& .card .meta": {
        textDecoration: "line-through"
    },
    "&&&&& .card .description": {
        margin: 0,
        color: "red"
    }
})

//COMPONENT=================================================================
function DiscountsSlider({ discounts }) {
    function createSlides() {
        return discounts.map(
            (item) => {
                const { image, name, price, discount, id } = item;
                return (
                    <Segment key={id}>
                        <Card as={Link} to={`/product/${id}`}>
                            <Image src={image} wrapped ui={false} />
                            <Card.Content>
                                <Card.Header textAlign="center">{name}</Card.Header>
                                <Card.Meta textAlign="center">{price.symbol}{price.retail.toFixed(2)}</Card.Meta>
                                <Card.Description as="h4" textAlign="center">
                                    {price.symbol}{price.outlet.toFixed(2)} ({discount.toFixed(0) + "% OFF"})
                                
                                </Card.Description>
                            </Card.Content>
                        </Card>
                    </Segment>
                )
            }
        )
    }

    function render() {
        const settings = {
            accessibility: true,
            arrows: false,
            nextArrow: false,
            prevArrow: false,
            autoplay: true,
            autoplaySpeed: 3000,
            dots: true,
            infinite: true,
            pauseOnHover: true,
            responsive: [
                { breakpoint: 10000, settings: { slidesToShow: 6, slidesToScroll: 3 } },
                { breakpoint: 992, settings: { slidesToShow: 4, slidesToScroll: 2 } },
                { breakpoint: 768, settings: { slidesToShow: 3, dots: false } },
                { breakpoint: 576, settings: { slidesToShow: 2, dots: false } }
            ]
        };
        return (
            <Slider {...settings} className={slickClass}>
                {createSlides()}
            </Slider>
        );
    }
    
    return render()
}

//EXPORT COMPONENT==========================================================
export default DiscountsSlider;