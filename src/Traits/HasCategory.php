<?php

namespace JutiaDev\Category\Traits;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use JutiaDev\Category\Models\Category;

trait HasCategory
{
    protected bool $defaultCascadeDelete = false;

    public function category(): BelongsTo
    {
        /** @var Model $this */
        return $this->belongsTo(
            Category::class,
            'category_id',
            'id'
        );
    }

    /**
     * cascadeDelete
     * Applicable only for the models using the HasCategory trait
     * If you want to delete all products when the associated category is deleted then set the $cascadeDelete to true,
     * Else if you want to keep the product but on only set the foreign key to null then set the $cascadeDelete to false
     *
     * @return bool
     */
    public function getCascadeDeleteValue(): bool
    {
        return $this->cascadeDelete ?? $this->defaultCascadeDelete;
    }

    public function getRelationshipName(): ?string
    {
        return $this->relationshipName ?? null;
    }

}
