import React, { useState } from "react"
import styled from "styled-components"
import { ObjectId } from "bson"
import useInterval from "./useInterval"

const Container = styled.div`
  width: 95%;
  display: flex;
  flex-direction: column;
  align-items: center;
`

const Table = styled.table`
  width: calc(100vw - 48px);
  margin: 24px;
  border-spacing: 0;
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.05);
  border-top: 0.5px solid rgba(0, 0, 0, 0.05);
  background-color: white;
`

const TableHeaders = styled.tr`
  font-size: 1.8rem;
`

const TableHeader = styled.th`
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.05);
  border-top: 0.5px solid rgba(0, 0, 0, 0.05);
  padding: 16px;
`

const Item = styled.tr`
  font-size: 1.8rem;
  padding: 24px 8px;
`

const Data = styled.td`
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.05);
  border-top: 0.5px solid rgba(0, 0, 0, 0.05);
  padding: 16px;
  text-align: center;
`

const Number = styled.p`
  flex: 1;
`

const Name = styled.p`
  flex: 1;
`

const Button = styled.div`
  margin: 0 auto;
  width: 180px;
  background-color: #ff814f;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  text-transform: uppercase;
  font-size: 1.2rem;
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 100ms ease-out;
  text-align: center;

  &:hover {
    transform: scale(1.05) translateY(-2px);
  }
`

export default function OrdersList(props) {
  const [orders, setOrders] = useState([])

  useInterval(() => {
    props.client.callFunction("get_orders").then(result => {
      setOrders(result.orders)
    })
  }, 1000)

  function sendOrder(orderId) {
    console.log(orderId)
    props.client
      .callFunction("set_sending_order", [new ObjectId(orderId)])
      .then(result => {
        alert("Order is being sent!")
      })
  }

  return (
    <Container>
      <Table>
        <thead>
          <TableHeaders>
            <TableHeader>Order Number</TableHeader>
            <TableHeader>Item</TableHeader>
            <TableHeader>Send Order</TableHeader>
          </TableHeaders>
        </thead>

        <tbody>
          {orders.map(order => (
            <Item key={order.number}>
              <Data>
                <Number>{order.number}</Number>
              </Data>
              <Data>
                <Name>{order.name}</Name>
              </Data>
              <Data>
                <Button onClick={() => sendOrder(order._id.toString())}>
                  Send Order
                </Button>
              </Data>
            </Item>
          ))}
        </tbody>
      </Table>
    </Container>
  )
}
