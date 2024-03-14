import React, { useState } from 'react';

const MatrixComponent = ({matrixData, coefficient, selectedOption, id, onDelete, onMatrixChange, onFillMatrixRandom, onSelectedOptionChange, onCoefficientChange }) => {
  const handleMatrixInputChange = (rowIndex, colIndex, event) => {
    const newValue = event.target.value;
    onMatrixChange(id, rowIndex, colIndex, newValue);
  };

  const handleFillRandom = () => {
    onFillMatrixRandom(id);
  };

  const handleDelete = () => {
    onDelete(id);
  };

  const handleSelectedOptionChange = (event) => {
    const newSelectedOption = event.target.value;
    onSelectedOptionChange(id, newSelectedOption);
  };

  const handleCoefficientChange = (event) => {
    const newCoefficient = parseFloat(event.target.value);
    onCoefficientChange(id, newCoefficient);
  };

  return (
    <div>
      <h2>Matrix {id}</h2>
      <table>
        <tbody>
          {matrixData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, colIndex) => (
                <td key={colIndex}>
                  <input
                    type="text"
                    value={cell}
                    onChange={(event) => handleMatrixInputChange(rowIndex, colIndex, event)}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div>
        <label>
          Коэффициент:
          <input
            type="number"
            value={coefficient}
            onChange={handleCoefficientChange}
          />
        </label>
      </div>
      <div>
        <label>
          Выберите опцию:
          <select value={selectedOption} onChange={handleSelectedOptionChange}>
            <option value="min">min</option>
            <option value="max">max</option>
          </select>
        </label>
      </div>
      <button onClick={handleFillRandom}>Заполнить случайными значениями</button>
      <button onClick={handleDelete}>Удалить матрицу</button>
    </div>
  );
};

export default MatrixComponent;
