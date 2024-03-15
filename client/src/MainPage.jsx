import React, { useState } from 'react';
import MatrixComponent from './MatrixComponent';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000' // замените на фактический URL вашего сервера
});

const MainPage = () => {
  const [rows, setRows] = useState(3); // Начальное количество строк
  const [columns, setColumns] = useState(3); // Начальное количество столбцов
  const [matrices, setMatrices] = useState([]); // Список созданных матриц
  const [idCounter, setIdCounter] = useState(0); // Счетчик для уникальных идентификаторов
  const [solution, setSolution] = useState(null);

  const handleCreateMatrix = () => {
    // Создаем новую матрицу с уникальным идентификатором
    const newMatrix = {
      id: idCounter,
      matrixData: Array.from({ length: rows }, () => Array(columns).fill(0)),
      coefficient: 1,
      selectedOption: 'max'
    };
    setMatrices([...matrices, newMatrix]);
    setIdCounter(idCounter + 1); // Увеличиваем счетчик идентификаторов
  };

  const handleDeleteMatrix = (id) => {
    // Удаляем матрицу с указанным идентификатором из списка
    const updatedMatrices = matrices.filter(matrix => matrix.id !== id);
    setMatrices(updatedMatrices);
  };

  const handleMatrixChange = (id, rowIndex, colIndex, value) => {
    // Изменяем данные в матрице с указанным идентификатором
    const updatedMatrices = matrices.map(matrix => {
      if (matrix.id === id) {
        const newMatrixData = [...matrix.matrixData];
        newMatrixData[rowIndex][colIndex] = value;
        return { ...matrix, matrixData: newMatrixData };
      }
      return matrix;
    });
    setMatrices(updatedMatrices);
  };

  const handleFillMatrixRandom = (id) => {
    // Заполняем матрицу с указанным идентификатором случайными значениями
    const minVal = parseFloat(prompt('Минимальное значение:', '0'));
    const maxVal = parseFloat(prompt('Максимальное значение:', '100'));
    const floatingPoint = prompt('Числа с плавающей точкой? (да/нет)', 'нет').toLowerCase() === 'да';
    const precision = floatingPoint ? parseInt(prompt('Сколько знаков после запятой?', '2')) : 0;

    const updatedMatrices = matrices.map(matrix => {
      if (matrix.id === id) {
        const randomMatrixData = matrix.matrixData.map(row => row.map(() => {
          const randomValue = Math.random() * (maxVal - minVal) + minVal;
          return floatingPoint ? randomValue.toFixed(precision) : Math.round(randomValue);
        }));
        return { ...matrix, matrixData: randomMatrixData, selectedOption: 'min' };
      }
      return matrix;
    });
    setMatrices(updatedMatrices);
  };

  const handleSelectedOptionChange = (id, newSelectedOption) => {
    const updatedMatrices = matrices.map(matrix => {
      if (matrix.id === id) {
        return { ...matrix, selectedOption: newSelectedOption };
      }
      return matrix;
    });
    setMatrices(updatedMatrices);
  };

  const handleCoefficientChange = (id, newCoefficient) => {
    const updatedMatrices = matrices.map(matrix => {
      if (matrix.id === id) {
        return { ...matrix, coefficient: newCoefficient };
      }
      return matrix;
    });
    setMatrices(updatedMatrices);
  };

  const handleRowsChange = (newRowCount) => {
    setRows(newRowCount);
    updateMatricesDimensions(newRowCount, columns);
  };

  const handleColumnsChange = (newColumnCount) => {
    setColumns(newColumnCount);
    updateMatricesDimensions(rows, newColumnCount);
  };

  const updateMatricesDimensions = (newRowCount, newColumnCount) => {
    const updatedMatrices = matrices.map(matrix => {
      const updatedMatrixData = [];
      for (let i = 0; i < newRowCount; i++) {
        const newRow = [];
        for (let j = 0; j < newColumnCount; j++) {
          if (i < matrix.matrixData.length && j < matrix.matrixData[i].length) {
            newRow.push(matrix.matrixData[i][j]);
          } else {
            newRow.push(0);
          }
        }
        updatedMatrixData.push(newRow);
      }
      return { ...matrix, matrixData: updatedMatrixData };
    });
    setMatrices(updatedMatrices);
  };

  const solveTasks = () => {
    // Создаем массив данных для отправки на сервер
    const payloads = matrices.map(matrix => ({
      matrix: matrix.matrixData,
      coefficient: matrix.coefficient,
      option: matrix.selectedOption
    }));

    // Отправляем POST запрос на сервер для решения задач
    api.post('/solve', payloads)
      .then(response => {
        console.log(response.data);
        setSolution(response.data);
      })
      .catch(error => {
        console.error('Error solving tasks:', error);
        setSolution(null);
        if (error.response && error.response.status === 400) {
          toast.error('Ошибка: Сумма коэффициентов не равна 1');
        }
        else if (error.response && error.response.status === 422){
          toast.error('Ошибка: Неправильно введены данные');
        } else {
          toast.error(`Ошибка ${error.response.status}: ${error.response.data.message}`);
        }
      });
  };

  return (
    <div>
      <h1>Название вашего приложения</h1>
      <label>
        Количество строк:
        <input
          type="number"
          value={rows}
          onChange={(e) => handleRowsChange(parseInt(e.target.value))}
        />
      </label>
      <label>
        Количество столбцов:
        <input
          type="number"
          value={columns}
          onChange={(e) => handleColumnsChange(parseInt(e.target.value))}
        />
      </label>
      {matrices.map(matrix => (
        <MatrixComponent
        key={matrix.id}
        matrixData={matrix.matrixData}
        coefficient={matrix.coefficient}
        selectedOption={matrix.selectedOption}
        id={matrix.id}
        onDelete={handleDeleteMatrix}
        onMatrixChange={handleMatrixChange}
        onFillMatrixRandom={handleFillMatrixRandom}
        onSelectedOptionChange={handleSelectedOptionChange}
        onCoefficientChange={handleCoefficientChange}
      />
      ))}
      <button onClick={handleCreateMatrix}>Создать новую матрицу</button>
      <button onClick={solveTasks}>Решить задачи</button>
      {solution && (
        <div>
          <h2>Матрица решения</h2>
          <table>
            <tbody>
              {solution.resh.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, colIndex) => (
                    <td key={colIndex}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Суммы произведений элементов</h2>
          <ul>
            {matrices.map((matrix, index) => (
              <li key={index}>Сумма произведений для матрицы {matrix.id}: {solution.sum_proizv[index]}</li>
            ))}
          </ul>

          <h2>Нормализованная сумма</h2>
          <p>{solution.normalized_sum}</p>
        </div>
      )}
      <ToastContainer />
    </div>
  );
};

export default MainPage;
