/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { ReactElement } from "react"
import {
  ButtonProps as ButtonPropsT,
  Kind,
  Size,
  StyledBorderlessIconButton,
  StyledIconButton,
  StyledLinkButton,
  StyledMinimalButton,
  StyledPrimaryButton,
  StyledSecondaryButton,
  StyledTertiaryButton,
  StyledPrimaryFormSubmitButton,
  StyledSecondaryFormSubmitButton,
  StyledHeaderButton,
  StyledModalAlertButton,
} from "./styled-components"

function Button({
  kind,
  size,
  disabled,
  onClick,
  fluidWidth,
  children,
  autoFocus,
  alertType,
}: ButtonPropsT): ReactElement {
  let ComponentType = StyledPrimaryButton

  if (kind === Kind.SECONDARY) {
    ComponentType = StyledSecondaryButton
  } else if (kind === Kind.TERTIARY) {
    ComponentType = StyledTertiaryButton
  } else if (kind === Kind.LINK) {
    ComponentType = StyledLinkButton
  } else if (kind === Kind.ICON) {
    ComponentType = StyledIconButton
  } else if (kind === Kind.BORDERLESS_ICON) {
    ComponentType = StyledBorderlessIconButton
  } else if (kind === Kind.MINIMAL) {
    ComponentType = StyledMinimalButton
  } else if (kind === Kind.PRIMARY_FORM_SUBMIT) {
    ComponentType = StyledPrimaryFormSubmitButton
  } else if (kind === Kind.SECONDARY_FORM_SUBMIT) {
    ComponentType = StyledSecondaryFormSubmitButton
  } else if (kind === Kind.HEADER_BUTTON) {
    ComponentType = StyledHeaderButton
  } else if (kind === Kind.MODAL_ALERT_BUTTON) {
    ComponentType = StyledModalAlertButton
  }

  return (
    <ComponentType
      kind={kind}
      size={size || Size.MEDIUM}
      fluidWidth={fluidWidth || false}
      disabled={disabled || false}
      onClick={onClick || (() => {})}
      autoFocus={autoFocus || false}
      alertType={alertType || null}
    >
      {children}
    </ComponentType>
  )
}
export type ButtonProps = ButtonPropsT
export { Kind, Size }
export default Button
