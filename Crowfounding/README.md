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