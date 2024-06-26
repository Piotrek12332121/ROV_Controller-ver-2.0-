/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dma.h"
#include "i2c.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "mpu6050.h"
#include "QMC5883.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
#define OFFSET 615
#define CENTIMETER_PER_BIT 2.067
#define BATTERY_VOLTS_PER_BIT 4.6 // in mV
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
MPU6050_t MPU6050;
QMC_t module;
float Compas_Value;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
int __io_putchar(int ch) {
HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, 0xFFFF);
return ch;
}

uint8_t velocities[10]={0};
uint16_t adc_values[2]={0};

float depth=0;
float battery_voltage=0;


int caluclate_depth(uint16_t raw_pressure_value){
	int estimated_depth_in_cm=(int)(raw_pressure_value-OFFSET)*CENTIMETER_PER_BIT;
	return estimated_depth_in_cm;
}
float calculate_battery_voltage(uint16_t raw_adc_data){
	int value=(int)raw_adc_data*BATTERY_VOLTS_PER_BIT;
	return value;

}
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_I2C1_Init();
  MX_USART2_UART_Init();
  MX_ADC1_Init();
  MX_TIM1_Init();
  MX_TIM3_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */

  HAL_UART_Receive_IT (&huart2, velocities, 4);
  HAL_ADC_Start_DMA(&hadc1, &adc_values, 2);

  HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_3);
  HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_4);
  __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1,300);
  __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2,300);
  __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_3,300);
  __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_4,300);

  while (MPU6050_Init(&hi2c1) == 1);
  QMC_init(&module, &hi2c1, 200);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  printf("-----| MPU6050 AND PWM TEST |-----\r\n ");
  while (1)
  {
	  MPU6050_Read_All(&hi2c1, &MPU6050);
	  QMC_read(&module);

	  	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1,200+(int)velocities[0]);        // A is left UP engine
	  	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2,200+(int)velocities[1]);        // B is right UP engine
	  	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_3,200+(int)velocities[2]);        // C is left forward engine
	  	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_4,200+(int)velocities[3]);        // D is right forward engine
	  	static int iterator=0;
	  	int depth=0;
	  	int battery_voltage=0;

	  	iterator++;
	  	if (iterator>500){
	  		depth=caluclate_depth(adc_values[0]);
	  		battery_voltage=calculate_battery_voltage(adc_values[1]);
	  		printf("<%d,%d,%d,%d,%d,%d,%d,%d,%d>\r\n",(int)velocities[0],(int)velocities[1],(int)velocities[2],(int)velocities[3],(int)MPU6050.KalmanAngleX,(int)MPU6050.KalmanAngleY,(int)module.heading,(int)depth,battery_voltage);
	  		iterator=0;
	  	}

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE2);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 25;
  RCC_OscInitStruct.PLL.PLLN = 168;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{


    if(huart->Instance == USART2){

    HAL_UART_Receive_IT(&huart2, velocities, 4);
	}
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
