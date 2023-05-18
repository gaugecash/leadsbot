### Contrato de Crowdfunding Refundable basado en OpenZeppelin
## Descripción
Este repositorio contiene un contrato inteligente de crowdfunding refundable implementado en Solidity y basado en los contratos estándar de OpenZeppelin. Este contrato permite la creación de una campaña de crowdfunding en la que los inversores pueden recibir un reembolso si la campaña no alcanza su meta de financiamiento.

## Funcionalidades
El contrato RefundableCrowdsale extiende el contrato Crowdsale de OpenZeppelin y añade una meta de financiamiento (fundingGoal). Guarda las contribuciones de cada inversor y si la meta de financiamiento no se alcanza cuando finaliza la venta, los inversores pueden reclamar un reembolso de sus contribuciones.

## Estructura del contrato
A continuación, se presenta la estructura básica del contrato RefundableCrowdsale:

```solidity
contract RefundableCrowdsale is Crowdsale {
    uint256 public fundingGoal;
    mapping(address => uint256) public contributions;
    event Refund(address investor, uint256 amount);
    constructor(uint256 _fundingGoal, uint256 _rate, address payable _wallet, IERC20 _token);
    function _preValidatePurchase(address _beneficiary, uint256 _weiAmount) internal;
    function finalize() public;
    function goalReached() public view returns (bool);
    function claimRefund(address payable _investor) public;
}


### Uso de OpenZeppelin
Este contrato utiliza la biblioteca OpenZeppelin para proporcionar implementaciones seguras y comprobadas de estándares de tokens como ERC20, así como contratos de crowdsale. OpenZeppelin es una biblioteca de contratos inteligentes abiertos y reutilizables que ha sido auditada para seguridad.

### Consideraciones de seguridad
Este es un ejemplo simplificado de cómo podría ser un contrato de crowdfunding refundable. Antes de utilizar este contrato en un entorno de producción, se deben considerar muchos otros aspectos, incluyendo una auditoría de seguridad completa, pruebas exhaustivas y posibles implicaciones legales.

## Descripción final del código:

Este código combina los contratos Crowdsale, TimedCrowdsale, RefundableCrowdsale, PostDeliveryCrowdsale, ReentrancyGuard y Pausable de OpenZeppelin para implementar un Crowdsale con la lógica adicional que deseas.

El contrato MyTokenCrowdsale es el contrato principal que hereda de los contratos mencionados.

Las variables _rate y _wallet determinan la tasa de conversión y la dirección donde se recopilan los fondos respectivamente.

La función buyTokens se modifica para incluir la lógica de seguimiento de la meta y la distribución de tokens.

La función _processPurchase se modifica para realizar un seguimiento del cumplimiento de la meta.

La función _finalization se modifica para distribuir los tokens si se alcanza la meta y habilitar los reembolsos si no se alcanza.

La función _forwardFunds se modifica para enviar los fondos al contrato de reembolso si no se alcanza la meta.
La función _preValidatePurchase se modifica para verificar si la compra excedería la meta.

Recuerda que este es solo un ejemplo para ilustrar cómo combinar los contratos y no incluye todas las funcionalidades adicionales que puedas necesitar. Asegúrate de adaptarlo a tus necesidades y realizar las pruebas adecuadas antes de desplegarlo en una red blockchain.