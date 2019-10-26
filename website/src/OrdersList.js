import React from "react"
import styled from "styled-components"

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

export default function OrdersList() {
  const orders = [
    { number: "2348932", name: "fanta" },
    { number: "9285794", name: "juice" },
    { number: "9273492", name: "fanta" },
    { number: "7541634", name: "juice" },
    { number: "6741974", name: "fanta" },
    { number: "1645887", name: "juice" }
  ]

  return (
    <Container>
      <Table>
        <TableHeaders>
          <TableHeader>Order Number</TableHeader>
          <TableHeader>Item</TableHeader>
          <TableHeader>Accept Order</TableHeader>
        </TableHeaders>

        {orders.map(order => (
          <Item>
            <Data>
              <Number>{order.number}</Number>
            </Data>
            <Data>
              <Name>{order.name}</Name>
            </Data>
            <Data>
              <Button>Accept Order</Button>
            </Data>
          </Item>
        ))}
      </Table>
    </Container>
  )
}
